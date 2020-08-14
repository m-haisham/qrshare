var links = document.getElementsByTagName("a");
document.getElementById("da-btn").addEventListener("click", (e) => {
  e.preventDefault();

  for (let link of links) {
    link.click();
  }
});
