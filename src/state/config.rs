use serde::Serialize;
use uuid::Uuid;

#[derive(Debug, Serialize)]
pub struct Config {
    pub protection: Protection,
}

#[derive(Debug, Serialize)]
pub enum Protection {
    Protected(PasswordConfig),
    None,
}

#[derive(Debug, Serialize)]
pub struct PasswordConfig {
    password: String,
    key: Uuid,
}

impl Config {
    pub fn new(password_option: Option<String>) -> Self {
        let protection = match password_option {
            Some(password) => Protection::Protected(PasswordConfig {
                password,
                key: Uuid::new_v4(),
            }),
            None => Protection::None,
        };

        Config { protection }
    }
}

impl PasswordConfig {
    pub fn key_str(&self) -> String {
        self.key.to_hyphenated().to_string()
    }

    pub fn matches_password(&self, value: &str) -> bool {
        self.password == value
    }

    pub fn matches_key(&self, value: &str) -> bool {
        self.key_str() == value
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_key_str() {
        let password = PasswordConfig {
            password: String::from(""),
            key: Uuid::parse_str("5d7fde23-b2be-4833-9693-5e8e8a308c17").unwrap(),
        };

        assert_eq!(password.key_str(), "5d7fde23-b2be-4833-9693-5e8e8a308c17");
        assert_ne!(password.key_str(), "5d7fde23-b2be-4833-2358-a308c17");
    }

    #[test]
    fn test_password_matches() {
        let password = PasswordConfig {
            password: String::from("123"),
            key: Uuid::new_v4(),
        };

        assert_eq!(password.matches_password("123"), true);
        assert_eq!(password.matches_password("1234"), false);
    }

    #[test]
    fn test_key_matches() {
        let password = PasswordConfig {
            password: String::from(""),
            key: Uuid::parse_str("5d7fde23-b2be-4833-9693-5e8e8a308c17").unwrap(),
        };

        assert_eq!(
            password.matches_key("5d7fde23-b2be-4833-9693-5e8e8a308c17"),
            true
        );
        assert_eq!(
            password.matches_key("5d7fde23-b2be-asaf-5e8e8a308c17"),
            false
        );
    }
}
