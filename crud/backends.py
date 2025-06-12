from django.contrib.auth.backends import BaseBackend
from .models import AdminAccounts, GuestAccounts
from datetime import datetime
import random
import time

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