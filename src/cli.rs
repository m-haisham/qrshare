use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct Args {
    /// Relative or absolute paths to share
    pub paths: Vec<String>,

    /// Login password for the session
    #[clap(short, long)]
    pub password: Option<String>,

    /// Server port
    #[clap(long)]
    pub port: Option<u16>,
}
