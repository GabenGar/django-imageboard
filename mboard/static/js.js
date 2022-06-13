"use strict";

function addTooltip() {
    document.querySelectorAll('.quote').forEach((elmnt) => {
            tippy(elmnt, {
                content: document.querySelector(elmnt.getAttribute('href')).cloneNode(true),
                placement: 'auto-end',
                maxWidth: 800,
            });
        }
    )
}

function expandImages() {
    document.querySelectorAll('.image').forEach((element) => element.addEventListener('click', expandImage));

    function expandImage(imgClicked) {
        imgClicked.preventDefault();
        this.hidden = true;
        let expandedImg = document.createElement('img');
        this.closest('.imagediv').className = 'imagediv-expanded';
        expandedImg.src = this.parentElement.href;
        // img.style.maxWidth = '1000px';
        expandedImg.style.width = '100%';
        this.parentNode.appendChild(expandedImg);
        expandedImg.addEventListener('click', function (e) {
            e.preventDefault();
            expandedImg.previousElementSibling.hidden = false;
            expandedImg.closest('.imagediv-expanded').className = 'imagediv';
            expandedImg.remove();
        });
    }
}

function showQuickPostForm() {
    const quickPostForm = document.getElementById('quickPostForm');
    const postsLinks = document.querySelectorAll('.post .postHeader .postLink, .opPost > .opPostHeader .postLink');
    const quickPostFormTextArea = document.querySelector('#quickPostForm > textarea');
    const postForm = document.querySelector('#postForm');
    document.querySelector('#quickPostForm > #id_image').required = false;  //pizdos
    for (let i = 0; i < postsLinks.length; i++) {
        postsLinks[i].addEventListener('click', setTextValue
        );
    }

    function setTextValue(e) {
        e.preventDefault();
        quickPostForm.hidden = false;
        if (!quickPostForm.hidden) {
            {
                const postId = this.closest('article').id;  // this === e.currentTarget
                quickPostFormTextArea.value += `>>${postId}\n`.replace('id', ''); // '>>id1234' => '>>1234' pizdos
                try {
                    if (window.getSelection().focusNode.parentElement.closest('article').id === this.closest('article').id) {
                        const selectedText = window.getSelection();
                        quickPostFormTextArea.value += '>';
                        quickPostFormTextArea.value += selectedText.toString();
                        quickPostFormTextArea.value += '\n';
                    }
                } catch (e) {
                }
                document.querySelector('#quickPostForm > #id_threadnum').value = this.closest('article').dataset['threadid'];
                if (!postForm.hidden) {
                    postForm.value = this.closest('article').dataset['threadid'];
                    postForm['text'].value = quickPostFormTextArea.value
                }
                quickPostFormTextArea.focus();
            }
        }
    }

    document.getElementById('closebutton').addEventListener('click', () => {
        quickPostForm.hidden = true;
        quickPostFormTextArea.value = '';
    });
}

function dragPostForm(elmnt) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        elmnt.parentNode.style.top = (elmnt.parentNode.offsetTop - pos2) + "px";
        elmnt.parentNode.style.left = (elmnt.parentNode.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

function focusTextArea() {
    document.querySelector('#postForm > textarea').focus();
}
