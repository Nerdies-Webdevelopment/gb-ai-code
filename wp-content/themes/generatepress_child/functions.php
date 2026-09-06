<?php
/**
 * GeneratePress Child Theme
 *
 * Project-specific PHP belongs here.
 * Do not copy the GeneratePress parent theme functions.php into this file.
 *
 * @package GeneratePress_Child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Register the child-theme stylesheet for the WordPress block editor.
 *
 * GeneratePress loads the active child theme style.css on the frontend,
 * so this project does not enqueue the same stylesheet again via
 * wp_enqueue_scripts().
 *
 * @return void
 */
function gpc_setup_editor_styles() {
	add_theme_support( 'editor-styles' );
	add_editor_style( 'style.css' );
}
add_action( 'after_setup_theme', 'gpc_setup_editor_styles' );

/**
 * Add a featured-image column to GenerateBlocks templates.
 *
 * The hook name depends on the GenerateBlocks template post type used by
 * the installed project. Revalidate this integration after plugin changes.
 *
 * @param array $columns Existing list-table columns.
 * @return array
 */
function gpc_featured_image_column( $columns ) {
	return array_slice( $columns, 0, 1, true )
		+ array(
			'featured_image' => esc_html__( 'Featured Image', 'generatepress-child' ),
		)
		+ array_slice( $columns, 1, null, true );
}
add_filter(
	'manage_gblocks_templates_posts_columns',
	'gpc_featured_image_column'
);

/**
 * Render the GenerateBlocks template featured-image column.
 *
 * @param string $column_name Current column name.
 * @param int    $post_id     Current post ID.
 * @return void
 */
function gpc_render_featured_image_column( $column_name, $post_id ) {
	if ( 'featured_image' !== $column_name ) {
		return;
	}

	if ( ! has_post_thumbnail( $post_id ) ) {
		return;
	}

	$thumbnail_id = get_post_thumbnail_id( $post_id );
	$url          = wp_get_attachment_image_url( $thumbnail_id, 'medium' );

	if ( ! $url ) {
		return;
	}
	?>
	<img
		data-id="<?php echo esc_attr( $thumbnail_id ); ?>"
		src="<?php echo esc_url( $url ); ?>"
		alt=""
		loading="lazy"
		decoding="async"
	/>
	<?php
}
add_action(
	'manage_gblocks_templates_posts_custom_column',
	'gpc_render_featured_image_column',
	10,
	2
);

/**
 * Print admin-only styling for the GenerateBlocks template thumbnail column.
 *
 * Printed once on the relevant list-table screen rather than once per row.
 *
 * @return void
 */
function gpc_featured_image_column_styles() {
	$screen = get_current_screen();

	if ( ! $screen || 'gblocks_templates' !== $screen->post_type ) {
		return;
	}
	?>
	<style>
		.post-type-gblocks_templates #featured_image {
			width: 150px;
		}

		.post-type-gblocks_templates
		td.featured_image.column-featured_image img {
			display: block;
			width: auto;
			max-width: 100%;
			height: auto;
		}
	</style>
	<?php
}
add_action( 'admin_head-edit.php', 'gpc_featured_image_column_styles' );
