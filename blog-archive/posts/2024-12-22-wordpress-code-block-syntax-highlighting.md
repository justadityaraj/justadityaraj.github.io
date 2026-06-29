---
title: "WordPress Code Block Syntax Highlighting Without Plugins"
date: "2024-12-22T03:33:45"
modified: "2024-12-23T14:38:22"
slug: "wordpress-code-block-syntax-highlighting"
original_url: "https://adityarajsingh.com/wordpress-code-block-syntax-highlighting/"
categories: ["WordPress"]
tags: ["Code Snippets"]
excerpt: "If you want to highlight code syntax on your blog without using any plugins, we can achieve this using Highlight.js, a lightweight JavaScript library that adds syntax highlighting to your code blocks with minimal impact on your site’s speed. For example, you can see that I'm using it in this blog itself. So let’s do […]"
---

# WordPress Code Block Syntax Highlighting Without Plugins

If you want to highlight code syntax on your blog without using any plugins, we can achieve this using <a href="https://github.com/highlightjs/highlight.js" class="ek-link" target="_blank" aria-label="Highlight.js (opens in a new tab)" rel="noreferrer noopener">Highlight.js</a>, a lightweight JavaScript library that adds syntax highlighting to your code blocks with minimal impact on your site’s speed.

For example, you can see that I'm using it in this blog itself. So let’s do it!

## Step 1: Add Highlight.js

1.  Open footer.php in your WordPress theme.
2.  Add the following code just before the closing tag.

``` wp-block-code
<link href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/styles/atom-one-dark.min.css" rel="stylesheet"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
```

If you're using a page builder that doesn't allow you to edit the footer.php file, you can check its documentation on how to load external JavaScript libraries.

Alternatively, you can try adding the script code using an HTML block and see if that works.

### How the Code Works?

The first line of the code loads a color theme, in this case atom one dark. The second line brings in the Highlight.js library, which does the work of recognizing and highlighting the code. The last line tells the browser to apply the highlighting to all the code blocks on the page.

You can find the Highlight.js themes <a href="https://cdnjs.com/libraries/highlight.js" class="ek-link" target="_blank" aria-label=" (opens in a new tab)" rel="noreferrer noopener">here</a>, and replace the first line of the code as per your preference.

## Step 2: Apply Default Font to Code Blocks

To ensure the code blocks use your website's default font, add the following CSS to your theme's stylesheet.

``` wp-block-code
/* Apply the website default font to code blocks */
pre, code {
    font-family: inherit;
    font-size: inherit;
    line-height: 1.5;
}
.hljs {
    font-family: inherit;
}
```

**Done!**

Now, your code blocks will be highlighted using Highlight.js, without the need for any plugins. This keeps your website fast and clean while enhancing the readability of your code.

## (Optional) Step 3: Add the "Copy code" button

1.  Add the following script code right after the code from step 1:

``` wp-block-code
<script>
    document.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll('pre code').forEach((codeBlock) => {
            const lineCount = codeBlock.innerText.split('\n').filter(line => line.trim() !== '').length;

            // Skip adding the button if there's only one line of code
            if (lineCount <= 1) {
                return;}

            const copyButton = document.createElement("button");
            copyButton.classList.add("copy-btn");
            copyButton.textContent = "Copy code";
            const codeContainer = document.createElement("div");
            codeContainer.style.position = "relative";
            codeBlock.parentNode.insertBefore(codeContainer, codeBlock);
            codeContainer.appendChild(codeBlock);
            codeContainer.appendChild(copyButton);
            copyButton.addEventListener("click", () => {
                const code = codeBlock.innerText;
                navigator.clipboard.writeText(code).then(() => {
                    copyButton.textContent = "Copied!";
                    setTimeout(() => {
                        copyButton.textContent = "Copy again";
                    }, 2000);
                }).catch((err) => {
                    console.error("Failed to copy text: ", err);
                });
            });
        });
    });
</script>
```

Then add this CSS:

``` wp-block-code
/* code snippets copy button */
.copy-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 5px 10px;
    font-size: 12px;
    background-color: rgba(42, 42, 42, 0.8);
    color: #fff;
    border: 1px solid rgba(85, 85, 85, 0.8);
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s ease, border-color 0.3s ease;
}

.copy-btn:hover {
    background-color: rgba(68, 68, 68, 0.9);
    border-color: rgba(102, 102, 102, 0.9);
}

.copy-btn:focus {
    outline: none;
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
}

.copy-btn:active {
    background-color: rgba(102, 102, 102, 1);
}
```

Now, you should see a "Copy" button alongside your code snippets, just like on this blog. The button won’t appear for single-line code snippets, but you can remove this behavior by deleting the *if (lineCount \<= 1) { return;}* from button script.
