import * as XLSX from "../js/";

const eventDate = $(".participants-list").data("event-date");

// ...

function exporterVersExcel() {
  // Créez un tableau de données à partir des éléments HTML
  const data = [];
  $(".participant").each(function () {
    const firstName = $(this)
      .find('.label:contains("Prénom")')
      .next()
      .text()
      .trim();
    const lastName = $(this)
      .find('.label:contains("Nom de famille")')
      .next()
      .text()
      .trim();
    const email = $(this)
      .find('.label:contains("E-mail")')
      .next()
      .text()
      .trim();
    data.push([firstName, lastName, email]);
  });

  // Créez un classeur Excel, ajoutez une feuille de calcul, etc.
  const ws = XLSX.utils.aoa_to_sheet([
    ["Prénom", "Nom de famille", "E-mail"],
    ...data,
  ]);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Participants");

  // Exportez le classeur Excel vers un fichier
  XLSX.writeFile(wb, `participants_${eventDate}.xlsx`);
}

$("#exportButton").click(exporterVersExcel);
