from textnode import TextNode
from textnode import TextType

print("Hello World!")

def main():
    dummy_textnode = TextNode("Test Link!", TextType.LINK, "https://github.com/CzarRamos")
    print(dummy_textnode)

if __name__ == "__main__":
    main()