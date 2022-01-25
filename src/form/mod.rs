use rocket::form::FromForm;

#[derive(Debug, FromForm)]
pub struct LoginForm<'r> {
    pub password: &'r str,
}
