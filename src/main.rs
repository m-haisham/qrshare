mod cli;
mod context;
mod endpoint;
mod form;
mod guard;
mod models;
mod state;
mod utils;

use std::sync::Mutex;

use clap::StructOpt;
use ring::rand::{SecureRandom, SystemRandom};
use rocket::config::Config;
use rocket::fs::FileServer;
use rocket_dyn_templates::Template;
use state::config::AppConfig;
use state::filesystem::{SharedPath, SharedPathState};

#[macro_use]
extern crate rocket;

fn secret_key() -> Vec<u8> {
    let mut key = vec![0; 256];
    let sr = SystemRandom::new();
    sr.fill(&mut key).expect("Failed to generate secret key");

    key
}

#[launch]
fn rocket() -> _ {
    let args = cli::Args::parse();
    let root = SharedPath::root(args.paths).unwrap();
    let path_state = SharedPathState::from(root);
    let config = AppConfig::new(args.password);

    let figment = Config::figment()
        .merge(("port", args.port.unwrap_or(8000)))
        .merge(("secret_key", secret_key()));

    rocket::custom(figment)
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
                endpoint::archive_dir,
            ],
        )
        .mount("/host", routes![endpoint::qr_code])
        .mount("/static", FileServer::from("static/"))
        .attach(Template::fairing())
}
