---
title: "Exclude Tracking Code for Logged-In Users In WordPress"
date: "2024-12-09T00:24:36"
modified: "2024-12-22T02:21:57"
slug: "exclude-code-for-logged-in-users-wordpress"
original_url: "https://adityarajsingh.com/exclude-code-for-logged-in-users-wordpress/"
categories: ["WordPress"]
tags: ["Code Snippets"]
excerpt: "If you’re using tracking tools like Google Analytics, Plausible, or Umami Analytics on your WordPress site, you might want to exclude your logged-in users / own page views to get more accurate data. Tracking your own visits can skew the results, making it harder to understand actual user behavior. Here’s a quick and easy way […]"
---

# Exclude Tracking Code for Logged-In Users In WordPress

If you’re using tracking tools like Google Analytics, Plausible, or Umami Analytics on your WordPress site, you might want to exclude your logged-in users / own page views to get more accurate data. Tracking your own visits can skew the results, making it harder to understand actual user behavior.

Here’s a quick and easy way to exclude tracking code for logged-in users on WordPress:

We’ll use a simple PHP function to check if the user is logged in. If they are, the tracking code will be excluded.

## Use This PHP Code

Install the <a href="https://wordpress.org/plugins/code-snippets/" class="ek-link" aria-label="&quot;Code Snippets&quot; plugin (opens in a new tab)" target="_blank" rel="noreferrer noopener">"Code Snippets" plugin</a> (recommended) or Go to your WordPress dashboard, open Appearance \> Theme File Editor, and add this code to the functions.php file.

``` wp-block-code
function is_user_logged_in_custom() {
    $user = wp_get_current_user();
    return $user->exists();  // Returns true if a user is logged in, false otherwise
}

function add_tracking_code_for_logged_out_users_in_header() {
    if (!is_user_logged_in_custom()) { // If the user is NOT logged in
        ?>
        <script defer src="https://example.com/script.js" data-website-id="example"></script> // Replace this with your tracking code script
        <?php
    }
}
add_action('wp_head', 'add_tracking_code_for_logged_out_users_in_header');
```

## Test It

Log in to WordPress and check the page source: the tracking code should not appear. Log out, and the tracking code should be injected into the page.

## Why This Works?

**is_user_logged_in_custom():** This function checks if the user is logged in. If the user is logged out, it will execute the tracking code.

**wp_head Hook:** This hook is used to place the tracking code in the header of the site, where analytics tools typically expect it.

That’s it! Now, your tracking code will only run for logged-out users, keeping your own visits out of the analytics data. This helps ensure that the data you see reflects actual user behavior, not your own activity.
