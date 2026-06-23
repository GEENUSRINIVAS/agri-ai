import json
from app import app, xgb_model, encoders
from flask import current_app

with app.app_context():
    try:
        from app import predict
        with app.test_request_context('/predict', method='POST', data={
            'commodity': 'Tomato',
            'state': 'Karnataka',
            'district': 'Bangalore Urban'
        }, headers={'X-Requested-With': 'XMLHttpRequest'}):
            # mock current_user
            class MockUser:
                is_authenticated = True
            
            from flask_login.utils import _get_user
            app.login_manager._login_disabled = True # Disable login for test
            
            response = predict()
            print("Response Data:", response.get_data(as_text=True))
    except Exception as e:
        import traceback
        traceback.print_exc()
