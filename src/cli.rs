use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
pub struct Args {
    /// Relative or absolute paths to share
    pub paths: Vec<String>,
}
