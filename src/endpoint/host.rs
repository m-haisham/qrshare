use image::{DynamicImage, ImageFormat, ImageOutputFormat, Luma};
use local_ip_address::local_ip;
use qrcode::QrCode;

#[derive(Responder)]
#[response(content_type = "image/png")]
pub struct QrImage(Vec<u8>);

#[get("/qrcode")]
pub fn qr_code() -> QrImage {
    let local_ip = local_ip().unwrap();
    let code = QrCode::new(local_ip.to_string().as_bytes()).unwrap();
    let image = code.render::<Luma<u8>>().build();
    let dynamic = DynamicImage::ImageLuma8(image);

    let mut bytes: Vec<u8> = vec![];
    dynamic
        .write_to(&mut bytes, ImageOutputFormat::from(ImageFormat::Png))
        .unwrap();

    QrImage(bytes)
}
