from semantic_router import Route, RouteLayer
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
    ]
)

sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ]
)

small_talk = Route(
    name='small_talk',
    utterances=[
        "Hii",
        "Hello",
        "How are you?",
        "What is your name?",
        "Are you a robot?",
        "What are you?",
        "What do you do?",
    ]
)

router = RouteLayer(encoder=encoder, routes=[faq, sql, small_talk])

if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)
    print(router("How are you?").name)