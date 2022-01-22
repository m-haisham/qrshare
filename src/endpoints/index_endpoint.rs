use rocket_dyn_templates::Template;
use serde::Serialize;

use crate::filesystem::{SharedPath, SharedType};
use rocket::State;

#[derive(Serialize)]
struct IndexContext<'a> {
    path: &'a SharedType,
}

#[get("/")]
pub fn index(shared_path: &State<SharedPath>) -> Template {
    println!("{:#?}", shared_path);
    let context = IndexContext {
        path: &shared_path.shared,
    };

    Template::render("index", &context)
}
