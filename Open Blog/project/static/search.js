
  function search() {
    var input, filter, cards, cardContainer, h5,p, title,content,aname, i;
    input = document.getElementById("searchbar");
    filter = input.value.toUpperCase();
    cardContainer = document.getElementById("myItems");
    cards = cardContainer.getElementsByClassName("col");
    for (i = 0; i < cards.length; i++) {
        title = cards[i].querySelector(".card-body h5.card-title");
        content = cards[i].querySelector(".card-body p.card-text");
        aname = cards[i].querySelector(".card-body p.aname");
        if (title.innerText.toUpperCase().indexOf(filter) > -1) {
            cards[i].style.display = "flex";
        } 
        else if (content.innerText.toUpperCase().indexOf(filter) > -1){
          cards[i].style.display = "flex";
        }
        else if (aname.innerText.toUpperCase().indexOf(filter) > -1){
          cards[i].style.display = "flex";
        }
        else {
            cards[i].style.display = "none";
        }
    }
}
