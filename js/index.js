// scp -r * pi@themightye.com:/var/www/html/swirled-world/
const DEFAULT_POEM_FONT_SIZE = 18,
  INCREASE_FONT_BY = 3;

function fetchReq(content) {
  fetch("php/create_poem.php?q=" + content)
    .then(function(response) {
      if (response.status !== 200) {
        console.log(
          "Looks like there was a problem. Status Code: " + response.status
        );
        $("#loading").hide();

        return;
      }

      // Examine the text in the response
      response.json().then(function(data) {
        $("#loading").hide();
        showPoem(data);
      });
    })
    .catch(function(err) {
      $("#loading").hide();
      console.log("Fetch Error :-S", err);
    });
}

function appendNode(type, id, clss, addTo) {
  let newNode = addTo.appendChild(document.createElement(type));
  if (id !== "") newNode.setAttribute("id", id);
  if (clss !== "") newNode.setAttribute("class", clss);
  return newNode;
}

function log(msg) {
  console.log(msg);
}

function showPoem(jsonResponse) {
  let wordsAndFonts = {};
  let poemContainerElm = $("#poem-container")[0];
  /* Clear the container */
  poemContainerElm.innerHTML = "";

  for (let i = 0; i < jsonResponse.length; i++) {
    for (let j = 0; j < jsonResponse[i].length; j++) {
      const word = jsonResponse[i][j];
      let spanElm = appendNode("span", "", "poemWord", poemContainerElm);
      spanElm.innerHTML = word + " ";
      if (wordsAndFonts.hasOwnProperty(word)) {
        spanElm.style.fontSize = wordsAndFonts[word] += INCREASE_FONT_BY;
      } else {
        wordsAndFonts[word] = DEFAULT_POEM_FONT_SIZE;
      }
    }
    appendNode("br", "", "", poemContainerElm);
  }
}

$("#poemForm").submit(function(e) {
  e.preventDefault();
  let inputText = $("#inputField").val();
  if (inputText === "") {
    alert("Input cannot be emtpy.");
    return;
  } else {
    const split = inputText.split(" ");
    if (split.length > 2) {
      alert("You can only enter maximum of two keywords.");
      return;
    }
  }
  $("#loading").show();
  fetchReq(inputText);
});
