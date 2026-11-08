# QR Code Generator and Viewer

import qrcode

def generate_qr():
    # Get input from user
    data = input("Enter text or URL for QR Code: ")

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(data)
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill_color="black", back_color="white")

    # Save image
    file_name = "generated_qr.png"
    img.save(file_name)

    print("QR Code generated successfully!")
    print(f"Saved as: {file_name}")

    # Display QR code
    img.show()

# Run the function
generate_qr()