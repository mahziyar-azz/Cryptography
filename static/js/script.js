function openTab(evt, tabName) {
    let i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        tabcontent[i].classList.remove("active");
    }
    tablinks = document.getElementsByClassName("tab-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}
function openSubTab(evt, subTabId) {
    const container = document.getElementById('encryption'); // scope to encryption tab
    const contents = container.getElementsByClassName('subtab-content');
    const links = container.getElementsByClassName('subtab-link');

    for (let i = 0; i < contents.length; i++) {
        contents[i].classList.remove('active');
        contents[i].style.display = 'none';
    }
    for (let j = 0; j < links.length; j++) {
        links[j].classList.remove('active');
    }
    document.getElementById(subTabId).style.display = 'block';
    document.getElementById(subTabId).classList.add('active');
    evt.currentTarget.classList.add('active');
}


function copyOutput(elementId) {
    const outputElement = document.getElementById(elementId);
    outputElement.select();
    document.execCommand("copy");
}


document.getElementById('base64-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const text = document.getElementById('base64-input').value;
    const action = document.querySelector('input[name="base64-action"]:checked').value;
    
    fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'base64', text, action })
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            document.getElementById('base64-output').value = `Error: ${data.error}`;
        } else {
            document.getElementById('base64-output').value = data.result;
        }
    });
});

document.getElementById('hashing-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const text = document.getElementById('hashing-input').value;
    const algorithm = document.querySelector('input[name="hash-algo"]:checked').value;

    fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'hash', text, algorithm })
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            document.getElementById('hashing-output').value = `Error: ${data.error}`;
        } else {
            document.getElementById('hashing-output').value = data.result;
        }
    });
});

document.getElementById('encryption-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const text = document.getElementById('encryption-input').value;
    const action = document.querySelector('input[name="aes256-action"]:checked').value;
    const key = document.getElementById('aes-key').value;

    fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'aes', text, action, key })
    })
    .then(response => response.json())
    .then(data => {
        if(data.error) {
            document.getElementById('encryption-output').value = `Error: ${data.error}`;
        } else {
            document.getElementById('encryption-output').value = data.result;
        }
    });
});

// AES-RSA subtab handler (enable your "Convert" button)
document.getElementById('aesrsa-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const text = document.getElementById('aesrsa-input').value;
    const action = document.querySelector('input[name="aesrsa-action"]:checked').value;
    const public_key = document.getElementById('rsa-public').value || null;
    const private_key = document.getElementById('rsa-private').value || null;

    fetch('/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'aes_rsa', text, action, public_key, private_key })
    })
    .then(r => r.json())
    .then(data => {
      document.getElementById('aesrsa-output').value = data.error ? `Error: ${data.error}` : data.result;
    });
  });
  


function clearFields(inputId, outputId) {
    document.getElementById(inputId).value = '';
    document.getElementById(outputId).value = '';
}

document.querySelectorAll('input[name="aes256-action"]').forEach(radio => {
    radio.addEventListener('change', () => clearFields('encryption-input', 'encryption-output'));
});

document.querySelectorAll('input[name="aesrsa-action"]').forEach(radio => {
    radio.addEventListener('change', () => clearFields('aesrsa-input', 'aesrsa-output'));
});

const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

function applyTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
        themeToggle.textContent = '☀️';
    } else {
        body.classList.remove('dark-mode');
        themeToggle.textContent = '🌙';
    }
}



themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
        themeToggle.textContent = '☀️';
    } else {
        localStorage.setItem('theme', 'light');
        themeToggle.textContent = '🌙';
    }
});





function setupRadioIconToggle(radioGroupName, iconMap) {
    const radios = document.querySelectorAll(`input[name="${radioGroupName}"]`);
    
    radios.forEach(radio => {
        radio.addEventListener('change', (event) => {

            const selectedRadio = event.target;
            const icon = selectedRadio.parentElement.querySelector('i');
            

            const iconName = iconMap[selectedRadio.value];
            if (icon && iconName) {
                icon.setAttribute('data-lucide', iconName);
                

                radios.forEach(otherRadio => {
                    if (otherRadio !== selectedRadio) {
                        const otherIcon = otherRadio.parentElement.querySelector('i');
                        const otherIconName = iconMap[otherRadio.value];
                        if (otherIcon && otherIconName) {
                            otherIcon.setAttribute('data-lucide', otherIconName);
                        }
                    }
                });
                lucide.createIcons();
            }
        });
    });
}
// --- Initial Setup on Page Load ---

document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('.tab-link').click();

    applyTheme();

    lucide.createIcons()




    
    setupRadioIconToggle('base64-action', {
        'encode': 'package',
        'decode': 'package-open'
    });

    setupRadioIconToggle('aes256-action', { 
        'encrypt': 'lock',
        'decrypt': 'lock-open' 
        });
    setupRadioIconToggle('aesrsa-action', {
        'encrypt': 'lock',
        'decrypt': 'lock-open'
    });
    
});
