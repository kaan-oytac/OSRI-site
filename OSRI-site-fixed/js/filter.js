// Publication tag filter. Progressive enhancement: the full list renders without JS.
(function () {
  var bars = document.querySelectorAll("[data-filter-for]");
  Array.prototype.forEach.call(bars, function (bar) {
    var list = document.getElementById(bar.getAttribute("data-filter-for"));
    if (!list) return;
    var buttons = bar.querySelectorAll("button[data-tag]");
    var entries = list.querySelectorAll("[data-tags]");
    var empty = list.querySelector("[data-empty]");

    function apply(tag) {
      var shown = 0;
      Array.prototype.forEach.call(entries, function (el) {
        var tags = (el.getAttribute("data-tags") || "").split(" ");
        var show = tag === "all" || tags.indexOf(tag) !== -1;
        el.hidden = !show;
        if (show) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
      Array.prototype.forEach.call(buttons, function (b) {
        b.setAttribute("aria-pressed", b.getAttribute("data-tag") === tag ? "true" : "false");
      });
    }

    Array.prototype.forEach.call(buttons, function (b) {
      b.addEventListener("click", function () { apply(b.getAttribute("data-tag")); });
    });
  });
})();
