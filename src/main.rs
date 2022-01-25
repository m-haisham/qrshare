mod cli;
mod context;
mod endpoint;
mod form;
mod guard;
mod state;

use std::sync::Mutex;

use clap::StructOpt;
use endpoint as ep;
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
    let config = Config::new(Some(String::from("123")));

    rocket::build()
        .manage(Mutex::new(path_state))
        .manage(config)
        .mount(
            "/",
            routes![
                ep::index,
                ep::index_redirect_login,
                ep::path,
                ep::path_redirect_login,
                ep::file,
                ep::file_redirect_login,
                ep::login,
                ep::login_post
            ],
        )
        .mount("/public", FileServer::from("static/"))
        .attach(Template::fairing())
}
