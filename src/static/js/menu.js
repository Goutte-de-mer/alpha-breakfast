// Sélectionne tous les éléments du menu principal qui ont un sous-menu
let menuItemsWithSubMenu = $(".dropdown-menu-link");

// Gestionnaire de clic à chaque élément du menu principal
menuItemsWithSubMenu.click(function () {
  // Trouvez le sous-menu correspondant à l'élément du menu cliqué
  let subMenu = $(this).children(".submenu");
  $(this).toggleClass("active");
  $(this).children(".fa-angle-down").toggleClass("rotate-180");

  // Utilisez la fonction slideToggle pour afficher ou masquer le sous-menu avec une animation
  subMenu.slideToggle();
});
