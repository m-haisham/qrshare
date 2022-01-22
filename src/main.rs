mod endpoints;
mod filesystem;

use endpoints::index;
use filesystem::{SharedPath};
use rocket::fs::FileServer;
use rocket_dyn_templates::Template;

#[macro_use]
extern crate rocket;

#[launch]
fn rocket() -> _ {
    let paths = vec![".".to_string()];
    let shared_path = SharedPath::from(paths).unwrap();

    rocket::build()
        .manage(shared_path)
        .mount("/", routes![index])
        .mount("/public", FileServer::from("static/"))
        .attach(Template::fairing())
}
