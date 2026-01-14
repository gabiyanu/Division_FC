"""
Export Module for Instagram-Ready Content

This module provides functions to export visualizations and animations
in formats optimized for Instagram (posts, stories, reels).

Usage:
    from src.export.instagram import InstagramExporter
    
    exporter = InstagramExporter()
    exporter.export_post(fig, "my_visualization.png")
    exporter.export_reel(animation, "my_animation.mp4")
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Optional, Tuple, Union
import subprocess
import os


class InstagramExporter:
    """
    A class for exporting visualizations in Instagram-optimized formats.
    """
    
    # Instagram dimensions
    POST_SIZE = (1080, 1080)        # Square post
    PORTRAIT_POST_SIZE = (1080, 1350)  # 4:5 portrait post
    STORY_SIZE = (1080, 1920)       # 9:16 story
    REEL_SIZE = (1080, 1920)        # 9:16 reel
    
    def __init__(self, output_dir: str = 'output'):
        """
        Initialize the exporter.
        
        Args:
            output_dir: Base output directory
        """
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / 'images'
        self.videos_dir = self.output_dir / 'videos'
        self.gifs_dir = self.output_dir / 'gifs'
        
        # Create directories
        for dir_path in [self.images_dir, self.videos_dir, self.gifs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def export_post(
        self,
        fig: Figure,
        filename: str,
        format: str = 'square',
        add_watermark: bool = False,
        watermark_text: str = '@yourusername',
        background_color: str = '#1a1a2e'
    ) -> str:
        """
        Export a figure as an Instagram post.
        
        Args:
            fig: Matplotlib figure to export
            filename: Output filename
            format: 'square' (1080x1080) or 'portrait' (1080x1350)
            add_watermark: Whether to add a watermark
            watermark_text: Text for watermark
            background_color: Background color for padding
            
        Returns:
            Path to saved file
        """
        size = self.POST_SIZE if format == 'square' else self.PORTRAIT_POST_SIZE
        
        # Save figure to temporary file
        temp_path = self.images_dir / f'temp_{filename}'
        fig.savefig(
            temp_path,
            dpi=150,
            bbox_inches='tight',
            facecolor=fig.get_facecolor(),
            edgecolor='none'
        )
        plt.close(fig)
        
        # Open and resize with PIL
        img = Image.open(temp_path)
        img = self._resize_with_padding(img, size, background_color)
        
        # Add watermark if requested
        if add_watermark:
            img = self._add_watermark(img, watermark_text)
        
        # Save final image
        output_path = self.images_dir / filename
        img.save(output_path, 'PNG', quality=95)
        
        # Clean up temp file
        temp_path.unlink()
        
        return str(output_path)
    
    def export_story(
        self,
        fig: Figure,
        filename: str,
        add_watermark: bool = False,
        watermark_text: str = '@yourusername',
        background_color: str = '#1a1a2e'
    ) -> str:
        """
        Export a figure as an Instagram story.
        
        Args:
            fig: Matplotlib figure to export
            filename: Output filename
            add_watermark: Whether to add a watermark
            watermark_text: Text for watermark
            background_color: Background color for padding
            
        Returns:
            Path to saved file
        """
        # Save figure to temporary file
        temp_path = self.images_dir / f'temp_{filename}'
        fig.savefig(
            temp_path,
            dpi=150,
            bbox_inches='tight',
            facecolor=fig.get_facecolor()
        )
        plt.close(fig)
        
        # Open and resize for story format
        img = Image.open(temp_path)
        img = self._resize_with_padding(img, self.STORY_SIZE, background_color)
        
        if add_watermark:
            img = self._add_watermark(img, watermark_text, position='bottom')
        
        # Save final image
        output_path = self.images_dir / filename
        img.save(output_path, 'PNG', quality=95)
        
        temp_path.unlink()
        
        return str(output_path)
    
    def export_reel(
        self,
        anim: animation.FuncAnimation,
        filename: str,
        fps: int = 30,
        duration: Optional[float] = None,
        add_watermark: bool = False,
        watermark_text: str = '@yourusername'
    ) -> str:
        """
        Export an animation as an Instagram reel.
        
        Args:
            anim: Matplotlib animation to export
            filename: Output filename
            fps: Frames per second
            duration: Maximum duration in seconds
            add_watermark: Whether to add watermark
            watermark_text: Watermark text
            
        Returns:
            Path to saved file
        """
        output_path = self.videos_dir / filename
        
        # Configure writer for Instagram-optimal settings
        writer = animation.FFMpegWriter(
            fps=fps,
            codec='libx264',
            bitrate=5000,
            extra_args=[
                '-vf', f'scale={self.REEL_SIZE[0]}:{self.REEL_SIZE[1]}:force_original_aspect_ratio=decrease,pad={self.REEL_SIZE[0]}:{self.REEL_SIZE[1]}:(ow-iw)/2:(oh-ih)/2:black',
                '-pix_fmt', 'yuv420p'  # Required for Instagram compatibility
            ]
        )
        
        anim.save(str(output_path), writer=writer, dpi=150)
        
        # Add watermark if requested (using ffmpeg)
        if add_watermark:
            self._add_video_watermark(output_path, watermark_text)
        
        return str(output_path)
    
    def export_gif(
        self,
        anim: animation.FuncAnimation,
        filename: str,
        fps: int = 15,
        optimize: bool = True,
        size: Tuple[int, int] = (540, 540)
    ) -> str:
        """
        Export an animation as an optimized GIF.
        
        Args:
            anim: Matplotlib animation to export
            filename: Output filename
            fps: Frames per second
            optimize: Whether to optimize GIF size
            size: Output size (smaller than Instagram for file size)
            
        Returns:
            Path to saved file
        """
        output_path = self.gifs_dir / filename
        
        # Use PillowWriter for GIFs
        writer = animation.PillowWriter(fps=fps)
        anim.save(str(output_path), writer=writer, dpi=100)
        
        # Optimize if requested
        if optimize:
            self._optimize_gif(output_path, size)
        
        return str(output_path)
    
    def _resize_with_padding(
        self,
        img: Image.Image,
        target_size: Tuple[int, int],
        background_color: str
    ) -> Image.Image:
        """Resize image and add padding to match target size."""
        # Calculate scaling factor
        width_ratio = target_size[0] / img.width
        height_ratio = target_size[1] / img.height
        ratio = min(width_ratio, height_ratio)
        
        # Resize image
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Create new image with background
        result = Image.new('RGB', target_size, background_color)
        
        # Paste resized image centered
        offset = ((target_size[0] - new_size[0]) // 2, (target_size[1] - new_size[1]) // 2)
        result.paste(img, offset)
        
        return result
    
    def _add_watermark(
        self,
        img: Image.Image,
        text: str,
        position: str = 'bottom_right',
        opacity: int = 180
    ) -> Image.Image:
        """Add a text watermark to an image."""
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fall back to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position
        padding = 20
        if position == 'bottom_right':
            x = img.width - text_width - padding
            y = img.height - text_height - padding
        elif position == 'bottom':
            x = (img.width - text_width) // 2
            y = img.height - text_height - padding
        else:
            x = padding
            y = img.height - text_height - padding
        
        # Draw text with slight shadow for visibility
        draw.text((x+1, y+1), text, font=font, fill=(0, 0, 0, opacity))
        draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))
        
        return img
    
    def _add_video_watermark(self, video_path: Path, text: str):
        """Add watermark to video using ffmpeg."""
        temp_path = video_path.with_suffix('.temp.mp4')
        
        try:
            subprocess.run([
                'ffmpeg', '-y', '-i', str(video_path),
                '-vf', f"drawtext=text='{text}':x=w-tw-20:y=h-th-20:fontsize=24:fontcolor=white@0.7",
                '-codec:a', 'copy',
                str(temp_path)
            ], check=True, capture_output=True)
            
            # Replace original with watermarked version
            temp_path.replace(video_path)
        except subprocess.CalledProcessError:
            # If ffmpeg fails, keep original without watermark
            if temp_path.exists():
                temp_path.unlink()
    
    def _optimize_gif(self, gif_path: Path, size: Tuple[int, int]):
        """Optimize GIF file size."""
        img = Image.open(gif_path)
        
        # Resize if needed
        if img.size != size:
            frames = []
            try:
                while True:
                    frame = img.copy().resize(size, Image.Resampling.LANCZOS)
                    frames.append(frame)
                    img.seek(img.tell() + 1)
            except EOFError:
                pass
            
            if frames:
                frames[0].save(
                    gif_path,
                    save_all=True,
                    append_images=frames[1:],
                    optimize=True,
                    duration=img.info.get('duration', 100),
                    loop=0
                )


def create_instagram_post(
    fig: Figure,
    filename: str,
    watermark: Optional[str] = None
) -> str:
    """Convenience function to create an Instagram post."""
    exporter = InstagramExporter()
    return exporter.export_post(
        fig, filename,
        add_watermark=bool(watermark),
        watermark_text=watermark or ''
    )
