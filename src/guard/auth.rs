use rocket::{
    http::{Cookie, CookieJar, Status},
    outcome::Outcome,
    request::{self, FromRequest, Request},
    State,
};

use crate::{
    form::LoginForm,
    state::config::{AppConfig, Protection},
};

const AUTH_KEY: &str = "auth";

#[derive(Debug)]
pub struct Auth;

#[derive(Debug)]
pub enum AuthError {
    BadConfigOutcome,
}

impl Auth {
    pub fn login(form: &LoginForm, cookiejar: &CookieJar, config: &AppConfig) -> bool {
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

    pub fn logout(cookiejar: &CookieJar) {
        cookiejar.remove_private(Cookie::named(AUTH_KEY))
    }
}

#[rocket::async_trait]
impl<'r> FromRequest<'r> for Auth {
    type Error = AuthError;

    async fn from_request(req: &'r Request<'_>) -> request::Outcome<Self, Self::Error> {
        let password = match req.guard::<NeedAuth>().await {
            Outcome::Success(s) => s.protection,
            Outcome::Failure(f) => return Outcome::Failure(f),
            Outcome::Forward(_) => return Outcome::Success(Auth),
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
        let password = match req.guard::<NeedAuth>().await {
            Outcome::Success(s) => s.protection,
            Outcome::Failure(f) => return Outcome::Failure(f),
            Outcome::Forward(_) => return Outcome::Forward(()),
        };

        let cookie = match req.cookies().get_private(AUTH_KEY) {
            Some(cookie) => cookie,
            None => return Outcome::Success(NotLoggedIn),
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
        let config_outcome = req.guard::<&State<AppConfig>>().await;
        let config = match config_outcome {
            Outcome::Success(config) => config,
            _ => return Outcome::Failure((Status::Conflict, AuthError::BadConfigOutcome)),
        };

        match &config.protection {
            Some(protection) => Outcome::Success(NeedAuth { protection }),
            None => Outcome::Forward(()),
        }
    }
}
