<?php
// === FONCTIONS LOUIS CHÈZE ===

// Ajout texte sous image produit (plugin WooCommerce) */

function skyverge_add_below_featured_image($product_id)
{
    echo '<h2 class="titre_sous_bouteille">' . get_the_title($product_id) . '</h2>';
    echo '<h3 class="sarl">sarl louis cheze</h3>';
    echo '<p style="text-align:center;margin-top:10px;color:white;font-size:15px;">«Pangon» <br>
    07340 LIMONY (France) <br>
    Tél : +33 (0)4 75 34 02 88 <br>
    Fax : +33 (0)4 75 34 13 25
</p>';
    echo '<a href="https://louischeze.com" style="color:#f9c978;">www.domainecheze.com</a>';
    echo '<img style="height:auto;transform: translate(0, -930%);"
    src="https://www.louischeze.com/wp-content/uploads/2017/04/logo-cheze-3.png">';
}
add_action('woocommerce_product_thumbnails', 'skyverge_add_below_featured_image', 9);

// Retire le prix du produit
remove_action('woocommerce_single_product_summary', 'woocommerce_template_single_price', 10);

// == A AIR D'AMES ==

// Ajout shortcode pour date de modification de la page
function last_modified_date_shortcode()
{
    $post_modified = get_the_modified_date();
    return $post_modified;
}
add_shortcode('last_modified_date', 'last_modified_date_shortcode');