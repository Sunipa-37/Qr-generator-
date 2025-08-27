from flask import Flask, render_template, request, send_file
import qrcode
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.get("qrdata")
        
        # generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # save QR code to memory instead of file
        buf = io.BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)

        return send_file(buf, mimetype="image/png", as_attachment=True, download_name="qrcode.png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
