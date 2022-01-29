mod cli;
mod context;
mod endpoint;
mod form;
mod guard;
mod state;

use std::sync::Mutex;

use clap::StructOpt;
use rocket::fs::FileServer;
use rocket_dyn_templates::Template;
use state::config::Config;
use state::filesystem::{SharedPath, SharedPathState};

#[macro_use]
extern crate rocket;

#[launch]
fn rocket() -> _ {
    let args = cli::Args::parse();
    let root = SharedPath::root(args.paths).unwrap();
    let path_state = SharedPathState::from(root);
    let config = Config::new(args.password);

    rocket::build()
        .manage(Mutex::new(path_state))
        .manage(config)
        .mount(
            "/",
            routes![
                endpoint::login_view,
                endpoint::logged_in,
                endpoint::login_form_submit,
                endpoint::home_view,
                endpoint::home_login_redirect,
                endpoint::path_view,
                endpoint::path_login_redirect,
                endpoint::file_serve,
                endpoint::file_login_redirect,
            ],
        )
        .mount("/host", routes![endpoint::qr_code])
        .mount("/static", FileServer::from("static/"))
        .attach(Template::fairing())
}
