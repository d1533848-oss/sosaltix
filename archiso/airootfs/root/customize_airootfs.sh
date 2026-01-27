
# Установка yay (AUR helper) и calamares
echo "Installing yay and calamares from AUR..."

# Создаем временного пользователя для сборки AUR пакетов
useradd -m -G wheel -s /bin/bash builder
echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Устанавливаем необходимые зависимости
pacman -S --needed --noconfirm git base-devel

# Переключаемся на пользователя builder для сборки
su - builder -c "
# Клонируем и устанавливаем yay
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si --noconfirm
cd ..

# Устанавливаем calamares через yay
yay -S --noconfirm calamares
"

# Удаляем временного пользователя
userdel -r builder

# Удаляем правило sudoers
sed -i '/builder ALL=(ALL) NOPASSWD: ALL/d' /etc/sudoers

# Включаем SDDM
systemctl enable sddm

# Включаем NetworkManager
systemctl enable NetworkManager

# Настраиваем часовой пояс по умолчанию
ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime

# Генерируем локали
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen

# Устанавливаем язык системы
echo "LANG=ru_RU.UTF-8" > /etc/locale.conf
echo "LC_COLLATE=C" >> /etc/locale.conf

# Устанавливаем hostname
echo "sosaltix" > /etc/hostname

# Добавляем хосты
cat > /etc/hosts << EOF
127.0.0.1    localhost
::1          localhost
127.0.1.1    sosaltix.localdomain    sosaltix
EOF

# Настройка sudo
echo "%wheel ALL=(ALL) ALL" >> /etc/sudoers
echo "Defaults timestamp_timeout=30" >> /etc/sudoers

# Создаём пользователя по умолчанию
useradd -m -G wheel,video,audio,storage -s /bin/bash liveuser
echo "liveuser:live" | chpasswd

# Настройка прав на polkit для Calamares
cat > /etc/polkit-1/rules.d/49-nopasswd-calamares.rules << EOF
polkit.addRule(function(action, subject) {
    if (action.id == "org.freedesktop.login1.reboot" ||
        action.id == "org.freedesktop.login1.reboot-multiple-sessions" ||
        action.id == "org.freedesktop.login1.power-off" ||
        action.id == "org.freedesktop.login1.power-off-multiple-sessions") {
        return polkit.Result.YES;
    }
});
EOF

# Копируем конфиги Calamares в нужные места
cp -r /etc/calamares /usr/share/calamares/
chmod -R 755 /usr/share/calamares/

# Создаём ярлык Calamares на рабочем столе
mkdir -p /etc/skel/Desktop
cat > /etc/skel/Desktop/install-sosaltix.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Установить Sosaltix
Comment=Установить Sosaltix на компьютер
Exec=calamares
Icon=system-installer
Terminal=false
Categories=System;
EOF

chmod +x /etc/skel/Desktop/install-sosaltix.desktop
cp /etc/skel/Desktop/install-sosaltix.desktop /home/liveuser/Desktop/

# Настраиваем Plasma для live-сессии
cat > /etc/skel/.config/plasma-localerc << EOF
[Formats]
LANG=ru_RU.UTF-8
EOF

# Устанавливаем тему курсора
ln -sf /usr/share/icons/breeze_cursors /usr/share/icons/default/cursors

# Завершаем настройку
echo "Sosaltix Live система готова!"
