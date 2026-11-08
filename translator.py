# Smart Document Translator (Python 3.14 Compatible)

from deep_translator import GoogleTranslator

def translate_text():
    print("===== SMART DOCUMENT TRANSLATOR =====\n")

    # Input text
    text = input("Enter the text to translate:\n")

    # Language code
    target_language = input(
        "\nEnter target language code "
        "(hi=Hindi, te=Telugu, kn=Kannada, fr=French, es=Spanish): "
    )

    try:
        # Translate text
        translated_text = GoogleTranslator(
            source="auto",
            target=target_language
        ).translate(text)

        print("\n===== TRANSLATED TEXT =====")
        print(translated_text)

        # Save translated text
        with open("translated_document.txt", "w", encoding="utf-8") as file:
            file.write(translated_text)

        print("\n✅ Translation saved in translated_document.txt")

    except Exception as e:
        print("\n❌ Error:", e)

if __name__ == "__main__":
    translate_text()