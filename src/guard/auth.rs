use rocket::{
    http::{Cookie, CookieJar, Status},
    outcome::Outcome,
    request::{self, FromRequest, Request},
    State,
};

use crate::{
    form::LoginForm,
    state::config::{Config, Protection},
};

const AUTH_KEY: &'static str = "auth";

#[derive(Debug)]
pub struct Auth;

#[derive(Debug)]
pub enum AuthError {
    BadConfigOutcome,
}

impl Auth {
    pub fn login(form: &LoginForm, cookiejar: &CookieJar, config: &Config) -> bool {
        let password = match &config.protection {
            Some(password_config) => password_config,
            None => return true,
        };

        if password.matches_password(form.password) {
            cookiejar.add_private(Cookie::new(AUTH_KEY, password.key_str()));
            true
        } else {
            false
        }
    }
}

#[rocket::async_trait]
impl<'r> FromRequest<'r> for Auth {
    type Error = AuthError;

    async fn from_request(req: &'r Request<'_>) -> request::Outcome<Self, Self::Error> {
        let need_auth_outcome = req.guard::<NeedAuth>().await;
        let password = match need_auth_outcome {
            Outcome::Success(s) => s.protection,
            Outcome::Failure(f) => return Outcome::Failure(f),
            Outcome::Forward(f) => return Outcome::Forward(f),
        };

        let cookie = match req.cookies().get_private(AUTH_KEY) {
            Some(cookie) => cookie,
            None => return Outcome::Forward(()),
        };

        if password.matches_key(cookie.value()) {
            Outcome::Success(Auth)
        } else {
            Outcome::Forward(())
        }
    }
}

#[derive(Debug)]
pub struct NotLoggedIn;

#[rocket::async_trait]
impl<'r> FromRequest<'r> for NotLoggedIn {
    type Error = AuthError;

    async fn from_request(req: &'r Request<'_>) -> request::Outcome<Self, Self::Error> {
        let need_auth_outcome = req.guard::<NeedAuth>().await;
        let password = match need_auth_outcome {
            Outcome::Success(s) => s.protection,
            Outcome::Failure(f) => return Outcome::Failure(f),
            Outcome::Forward(f) => return Outcome::Success(NotLoggedIn),
        };

        let cookie = match req.cookies().get_private(AUTH_KEY) {
            Some(cookie) => cookie,
            None => return Outcome::Forward(()),
        };

        if password.matches_key(cookie.value()) {
            Outcome::Forward(())
        } else {
            Outcome::Success(NotLoggedIn)
        }
    }
}

#[derive(Debug)]
pub struct NeedAuth<'a> {
    pub protection: &'a Protection,
}

#[rocket::async_trait]
impl<'r> FromRequest<'r> for NeedAuth<'r> {
    type Error = AuthError;

    async fn from_request(req: &'r Request<'_>) -> request::Outcome<Self, Self::Error> {
        let config_outcome = req.guard::<&State<Config>>().await;
        let config = match config_outcome {
            Outcome::Success(config) => config,
            _ => return Outcome::Failure((Status::Conflict, AuthError::BadConfigOutcome)),
        };

        let password = match &config.protection {
            Some(protection) => return Outcome::Success(NeedAuth { protection }),
            None => return Outcome::Forward(()),
        };
    }
}
