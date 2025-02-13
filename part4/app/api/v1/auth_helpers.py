from flask_jwt_extended import get_jwt, verify_jwt_in_request

def is_admin_user():
    try:
        verify_jwt_in_request()  # ✅ Ensure JWT is verified before calling get_jwt()
        claims = get_jwt()
        return claims.get("is_admin", False)
    except RuntimeError:
        return False  # Prevents error if JWT is not present