mod endpoints;
mod filesystem;
mod state;

use std::sync::Mutex;

use endpoints as ep;
use filesystem::{SharedPath, SharedPathState};
use rocket::fs::FileServer;
use rocket_dyn_templates::Template;

#[macro_use]
extern crate rocket;

#[launch]
fn rocket() -> _ {
    let paths = vec![".".to_string()];
    let root = SharedPath::root(paths).unwrap();
    let path_state = SharedPathState::from(root);

    rocket::build()
        .manage(Mutex::new(path_state))
        .mount("/", routes![ep::index, ep::path, ep::file])
        .mount("/public", FileServer::from("static/"))
        .attach(Template::fairing())
}
