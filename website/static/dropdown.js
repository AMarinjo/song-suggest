$(document).ready(function () {
    var input = $("#searchQueryInput");
    var autocompleteContainer = $("<div class='autocomplete-items'></div>");

    input.after(autocompleteContainer);

    input.on("input", function () {
        var inputValue = $(this).val();

        autocompleteContainer.html("");
        console.log(input);

        if (inputValue.length >= 2) {
            setTimeout(function () {
                fetch("/search?query=" + encodeURIComponent(inputValue))
                    .then(response => response.json())
                    .then(data => {
                        data.suggestions.forEach(function (suggestion) {
                            var trackName = suggestion.track_name.toString();
                            var matchStart = trackName.toLowerCase().indexOf(inputValue.toLowerCase());
                            var matchEnd = matchStart + inputValue.length;
                            var suggestionItem = $("<div></div>")
                                .html(trackName.substring(0, matchStart) + "<strong>" + trackName.substring(matchStart, matchEnd) + "</strong>" + trackName.substring(matchEnd))
                                .attr("data-redirect-url", suggestion.redirect_url)
                                .on("click", function () {
                                    var redirectUrl = $(this).data("redirect-url");
                                    if (redirectUrl) {
                                        window.location.href = redirectUrl;
                                    } else {
                                        input.val(trackName);
                                        autocompleteContainer.html("");
                                    }
                                });
                            autocompleteContainer.append(suggestionItem);
                        });
                        autocompleteContainer.width(input.outerWidth());
                    })
                    .catch(error => console.error("Error fetching suggestions:", error));
            }, 300);
        }
    });

    input.on("focus", function () {
        autocompleteContainer.css("border-color", "#ccc");
    });

    input.on("blur", function () {
        autocompleteContainer.css("border-color", "transparent");
    });

    $(document).on("click", function (e) {
        if (!$(e.target).is(input) && !$(e.target).is(autocompleteContainer)) {
            autocompleteContainer.html("");
        }
    });
});