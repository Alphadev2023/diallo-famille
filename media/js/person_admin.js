document.addEventListener("DOMContentLoaded", function () {
  const genderField = document.querySelector("#id_genre");
  const militaryRow = document.querySelector(".form-row.field-mari");

  function toggleMilitaryRank() {
    if (!genderField || !militaryRow) return;

    if (genderField.value === "F") {
      militaryRow.style.display = "";
    } else {
      militaryRow.style.display = "none";
    }
  }

  toggleMilitaryRank(); // Initial load
  genderField.addEventListener("change", toggleMilitaryRank);
});
