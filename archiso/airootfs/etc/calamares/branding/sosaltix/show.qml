import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation
{
    id: presentation

    function nextSlide() {
        console.log("QML Component (default slideshow) Next slide");
        presentation.goToNextSlide();
    }

    Timer {
        id: advanceTimer
        interval: 5000
        running: true
        repeat: true
        onTriggered: nextSlide()
    }

    Slide {
        Image {
            id: background1
            source: "slide1.png"
            width: 800; height: 450
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
        Text {
            anchors.horizontalCenter: background1.horizontalCenter
            anchors.top: background1.bottom
            text: "Добро пожаловать в Sosaltix"
            font.pixelSize: 24
            color: "#2c3e50"
        }
    }

    Slide {
        Image {
            id: background2
            source: "slide2.png"
            width: 800; height: 450
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
        Text {
            anchors.horizontalCenter: background2.horizontalCenter
            anchors.top: background2.bottom
            text: "Современный KDE Plasma"
            font.pixelSize: 24
            color: "#2c3e50"
        }
    }

    Slide {
        Image {
            id: background3
            source: "slide3.png"
            width: 800; height: 450
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
        Text {
            anchors.horizontalCenter: background3.horizontalCenter
            anchors.top: background3.bottom
            text: "Простая установка с Calamares"
            font.pixelSize: 24
            color: "#2c3e50"
        }
    }
}

