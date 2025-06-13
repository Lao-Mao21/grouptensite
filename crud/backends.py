from django.contrib.auth.backends import BaseBackend
from .models import AdminAccounts, GuestAccounts
from datetime import datetime
import random
import time
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

stripe.api_key = settings.STRIPE_SECRET_KEY

class AdminAccountsBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = AdminAccounts.objects.get(username=username)
            if user.check_password(password):
                return user
        except AdminAccounts.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AdminAccounts.objects.get(pk=user_id)
        except AdminAccounts.DoesNotExist:
            return None

class GuestAccountsBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = GuestAccounts.objects.get(username=username)
            if user.check_password(password):
                return user
        except GuestAccounts.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return GuestAccounts.objects.get(pk=user_id)
        except GuestAccounts.DoesNotExist:
            return None

class MockPaymentService:
    """Mock payment service to emulate payment processing"""
    
    @staticmethod
    def process_payment(payment_data):
        """
        Process a payment transaction
        Args:
            payment_data (dict): Payment information including:
                - amount: float
                - currency: str
                - payment_method: str (credit_card/gcash)
                - card_number: str (for credit cards)
                - gcash_number: str (for gcash)
        Returns:
            dict: Transaction result
        """
        # Simulate processing delay
        time.sleep(1)
        
        # Generate a mock transaction ID
        transaction_id = f"TXN_{datetime.now().strftime('%Y%m%d')}_{random.randint(1000, 9999)}"
        
        # Simulate success rate (90% success, 10% failure)
        is_successful = random.random() < 0.9
        
        if not is_successful:
            return {
                'success': False,
                'error': 'Payment declined by issuer',
                'transaction_id': transaction_id,
                'error_code': 'PAYMENT_DECLINED'
            }
        
        # Success response
        response = {
            'success': True,
            'transaction_id': transaction_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'COMPLETED',
            'payment_method': payment_data.get('payment_method'),
            'amount': payment_data.get('amount'),
            'currency': payment_data.get('currency', 'PHP'),
        }
        
        # Add method-specific details
        if payment_data.get('payment_method') == 'credit_card':
            response['card_last4'] = payment_data.get('card_number', '')[-4:]
            response['card_type'] = MockPaymentService._detect_card_type(payment_data.get('card_number', ''))
        elif payment_data.get('payment_method') == 'gcash':
            response['gcash_number'] = f"*****{payment_data.get('gcash_number', '')[-4:]}"
        
        return response
    
    @staticmethod
    def _detect_card_type(card_number):
        """Detect credit card type based on number"""
        if not card_number:
            return 'Unknown'
        
        # Remove spaces and non-digit characters
        card_number = ''.join(filter(str.isdigit, card_number))
        
        if card_number.startswith('4'):
            return 'Visa'
        elif card_number.startswith(('51', '52', '53', '54', '55')):
            return 'MasterCard'
        elif card_number.startswith(('34', '37')):
            return 'American Express'
        return 'Unknown'
    
    @staticmethod
    def verify_payment(transaction_id):
        """
        Verify a payment transaction
        Args:
            transaction_id (str): Transaction ID to verify
        Returns:
            dict: Verification result
        """
        # In a real system, this would query the payment gateway
        # For mock purposes, we'll always return success for valid transaction IDs
        if transaction_id and transaction_id.startswith('TXN_'):
            return {
                'success': True,
                'status': 'VERIFIED',
                'transaction_id': transaction_id,
                'verification_timestamp': datetime.now().isoformat()
            }
        
        return {
            'success': False,
            'error': 'Invalid transaction ID',
            'error_code': 'INVALID_TRANSACTION'
        }

class StripePaymentService:
    """Stripe payment service to handle payment processing"""
    
    @staticmethod
    def create_payment_intent(amount, currency='php', payment_method_types=None):
        """
        Create a PaymentIntent with Stripe
        Args:
            amount: float (amount in PHP)
            currency: str (default: 'php')
            payment_method_types: list of payment methods to accept
        Returns:
            dict: Payment intent details
        """
        if payment_method_types is None:
            payment_method_types = ['card']
            
        try:
            # Convert amount to cents/smallest currency unit
            amount_in_cents = int(amount * 100)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency=currency,
                payment_method_types=payment_method_types,
                metadata={
                    'integration_check': 'accept_a_payment',
                }
            )
            
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'amount': amount,
                'currency': currency.upper()
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': e.code if hasattr(e, 'code') else 'stripe_error'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': 'server_error'
            }
    
    @staticmethod
    def confirm_payment(payment_intent_id):
        """
        Confirm a payment intent
        Args:
            payment_intent_id: str
        Returns:
            dict: Confirmation result
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'success': True,
                'status': intent.status,
                'amount': intent.amount / 100,  # Convert from cents back to original currency
                'currency': intent.currency.upper(),
                'payment_method': intent.payment_method_types[0],
                'created': datetime.fromtimestamp(intent.created).isoformat()
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': e.code if hasattr(e, 'code') else 'stripe_error'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': 'server_error'
            }
    
    @staticmethod
    def refund_payment(payment_intent_id, amount=None):
        """
        Refund a payment
        Args:
            payment_intent_id: str
            amount: float (optional - if not provided, full amount will be refunded)
        Returns:
            dict: Refund result
        """
        try:
            refund_params = {'payment_intent': payment_intent_id}
            if amount:
                refund_params['amount'] = int(amount * 100)
                
            refund = stripe.Refund.create(**refund_params)
            
            return {
                'success': True,
                'refund_id': refund.id,
                'status': refund.status,
                'amount': refund.amount / 100,
                'currency': refund.currency.upper()
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': e.code if hasattr(e, 'code') else 'stripe_error'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': 'server_error'
            }

def guest_login_required(view_func):
    """
    Decorator for views that checks that the user is logged in as a guest,
    redirecting to the landing page if necessary.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'guest_id' not in request.session:
            messages.error(request, 'Please login to access this page.')
            return redirect('landing_page')
        return view_func(request, *args, **kwargs)
    return _wrapped_view