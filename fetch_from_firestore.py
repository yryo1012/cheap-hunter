from firebase_admin import firestore
from google.cloud.firestore import FieldFilter

db = firestore.client()

def fetch_latest_price(user_id, product_id):
    try:
        # Query Firestore
        docs = db.collection('products') \
            .order_by('created_at', direction=firestore.Query.DESCENDING) \
            .where(filter=FieldFilter('product_id', '==', product_id)) \
            .where(filter=FieldFilter('user_id', '==', user_id)) \
            .order_by('__name__', direction=firestore.Query.ASCENDING) \
            .limit(1) \
            .stream()

        for doc in docs:
            return doc.to_dict().get('price')

        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None