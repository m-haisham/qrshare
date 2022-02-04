use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct LoginContext<'a> {
    message: Option<&'a str>,
}

impl<'a> LoginContext<'a> {
    pub fn with(message: Option<&'a str>) -> Self {
        Self { message }
    }
}
