package mine.images;

import javax.swing.JLabel;
import javax.swing.ImageIcon;
import javax.swing.SwingConstants;

import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

import java.io.IOException;

public class JImage extends JLabel {
    private BufferedImage img;

    public JImage(String srcPath) {
        File file = null;

        try {
            file = new File(srcPath);
            img = ImageIO.read(file);
        } catch(IOException e) {
            System.out.println(e);
        }
    }

    public BufferedImage getImg() {
        return img;
    }

    public JLabel getLabel() {
        JLabel label = new JLabel();

        ImageIcon icon = new ImageIcon(img);
        label.setIcon(icon);
        label.setHorizontalAlignment(SwingConstants.CENTER);
        label.setVerticalAlignment(SwingConstants.CENTER);

        return label;
    }

    public JLabel getLabel(double aspectRatio) {
        JLabel label = new JLabel();

        int width = (int)(img.getWidth() * aspectRatio);
        int height = (int)(img.getHeight() * aspectRatio);
        ImageIcon imgIco = new ImageIcon(img);
        ImageIcon icon = new ImageIcon(imgIco.getImage().getScaledInstance(width, height, Image.SCALE_SMOOTH));

        label.setIcon(icon);
        label.setHorizontalAlignment(SwingConstants.CENTER);
        label.setVerticalAlignment(SwingConstants.CENTER);

        return label;
    }

    public BufferedImage img2Gray() {
        int width = img.getWidth();
        int height = img.getHeight();

        int[] pixels = img.getRGB(0, 0, width, height, null, 0, width);

        for(int i = 0; i < pixels.length; i++) {
            int p = pixels[i];

            int a = (p >> 24) & 0xff;
            int r = (p >> 16) & 0xff;
            int g = (p >> 8) & 0xff;
            int b = p & 0xff;

            int avg = (r + g + b)/3;

            p = (a << 24) | (avg << 16) | (avg << 8) | avg;

            pixels[i] = p;
        }

        img.setRGB(0, 0, width, height, pixels, 0, width);
        return img;
    }

    public BufferedImage img2GrayRed() {
        int width = img.getWidth();
        int height = img.getHeight();

        int[] pixels = img.getRGB(0, 0, width, height, null, 0, width);

        for(int i = 0; i < pixels.length; i++) {
            int p = pixels[i];

            int a = (p >> 24) & 0xff;
            int r = (p >> 16) & 0xff;
            int g = (p >> 16) & 0xff;
            int b = (p >> 16) & 0xff;

            int avg = (r + g + b)/3;

            p = (a<<24) | (avg<<16) | (avg<<8) | avg;

            pixels[i] = p;
        }

        img.setRGB(0, 0, width, height, pixels, 0, width);
        return img;
    }

    public BufferedImage img2GrayGreen() {
        int width = img.getWidth();
        int height = img.getHeight();

        int[] pixels = img.getRGB(0, 0, width, height, null, 0, width);

        for(int i = 0; i < pixels.length; i++) {
            int p = pixels[i];

            int a = (p >> 24) & 0xff;
            int r = (p >> 8) & 0xff;
            int g = (p >> 8) & 0xff;
            int b = (p >> 8) & 0xff;

            int avg = (r + g + b)/3;

            p = (a<<24) | (avg<<16) | (avg<<8) | avg;

            pixels[i] = p;
        }

        img.setRGB(0, 0, width, height, pixels, 0, width);
        return img;
    }

    public BufferedImage img2GrayBlue() {
        int width = img.getWidth();
        int height = img.getHeight();

        int[] pixels = img.getRGB(0, 0, width, height, null, 0, width);

        for(int i = 0; i < pixels.length; i++) {
            int p = pixels[i];

            int a = (p >> 24) & 0xff;
            int r = p & 0xff;
            int g = p & 0xff;
            int b = p & 0xff;

            int avg = (r + g + b)/3;

            p = (a<<24) | (avg<<16) | (avg<<8) | avg;

            pixels[i] = p;
        }

        img.setRGB(0, 0, width, height, pixels, 0, width);
        return img;
    }

    public BufferedImage img2Red() {
        int width = img.getWidth();
        int height = img.getHeight();

        int[] pixels = img.getRGB(0, 0, width, height, null, 0, width);

        for(int i = 0; i < pixels.length; i++) {
            int p = pixels[i];
            int r = (p >> 16) & 0xff;
            pixels[i] = (r << 16);
        }

        img.setRGB(0, 0, width, height, pixels, 0, width);
        return img;
    }

    public BufferedImage img2Green() {
        int width = img.getWidth();
        int height = img.getHeight();

        int[] pixels = img.getRGB(0, 0, width, height, null, 0, width);

        for(int i = 0; i < pixels.length; i++) {
            int p = pixels[i];
            int g = (p >> 8) & 0xff;
            pixels[i] = (g << 8);
        }

        img.setRGB(0, 0, width, height, pixels, 0, width);
        return img;
    }

    public BufferedImage img2Blue() {
        int width = img.getWidth();
        int height = img.getHeight();

        int[] pixels = img.getRGB(0, 0, width, height, null, 0, width);

        for(int i = 0; i < pixels.length; i++) {
            int p = pixels[i];
            int b = p & 0xff;
            pixels[i] = b;
        }

        img.setRGB(0, 0, width, height, pixels, 0, width);
        return img;
    }

    public BufferedImage img2Yellow() {
        int width = img.getWidth();
        int height = img.getHeight();

        int[] pixels = img.getRGB(0, 0, width, height, null, 0, width);

        for(int i = 0; i < pixels.length; i++) {
            int p = pixels[i];
            int r = (p >> 16) & 0xff;
            int g = (p >> 8) & 0xff;
            pixels[i] = (r << 16) | (g << 8);
        }

        img.setRGB(0, 0, width, height, pixels, 0, width);
        return img;
    }

    public void saveImage(String dstPath) {
        try {
            File file = new File(dstPath);
            ImageIO.write(img, "png", file);
        } catch(IOException e){
            System.out.println(e);
        }
    }

    public void saveImage(String dstPath, BufferedImage image) {
        try {
            File file = new File(dstPath);
            ImageIO.write(image, "png", file);
        } catch(IOException e){
            System.out.println(e);
        }
    }
}

