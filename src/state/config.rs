use serde::Serialize;
use uuid::Uuid;

#[derive(Debug, Serialize)]
pub struct AppConfig {
    pub protection: Option<Protection>,
}

#[derive(Debug, Serialize)]
pub struct Protection {
    password: String,
    key: Uuid,
}

impl AppConfig {
    pub fn new(password_option: Option<String>) -> Self {
        let protection = password_option.map(|password| Protection {
            password,
            key: Uuid::new_v4(),
        });

        AppConfig { protection }
    }
}

impl Protection {
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
        let password = Protection {
            password: String::from(""),
            key: Uuid::parse_str("5d7fde23-b2be-4833-9693-5e8e8a308c17").unwrap(),
        };

        assert_eq!(password.key_str(), "5d7fde23-b2be-4833-9693-5e8e8a308c17");
        assert_ne!(password.key_str(), "5d7fde23-b2be-4833-2358-a308c17");
    }

    #[test]
    fn test_password_matches() {
        let password = Protection {
            password: String::from("123"),
            key: Uuid::new_v4(),
        };

        assert_eq!(password.matches_password("123"), true);
        assert_eq!(password.matches_password("1234"), false);
    }

    #[test]
    fn test_key_matches() {
        let password = Protection {
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
