import qrcode
from io import BytesIO

def qrcode_generation(identity: str):
    # creating QRCode Object
    qr_object = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    # forming qrcode with the data passed in
    qr_object.add_data(identity)
    qr_object.make(fit=True)

    # creating a stream object [memory]
    stream_object = BytesIO()

    # make the qrcode image and save into stream object
    image = qr_object.make_image(fill_color="black", back_color="white")
    image.save(stream_object, format="JPEG")

    # get the value of stream object
    jpeg_data = stream_object.getvalue()

    return jpeg_data