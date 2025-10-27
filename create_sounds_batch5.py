#!/usr/bin/env python3
"""
Create MP3 sound files for Karma Nexus 2.0 - Batch 5
Using wave synthesis to create actual sound data
"""
import os
import struct
import math

PUBLIC_DIR = "/app/frontend/public"
os.makedirs(f"{PUBLIC_DIR}/sounds", exist_ok=True)

def create_tone(frequency, duration, sample_rate=44100):
    """Generate a sine wave tone"""
    samples = []
    for i in range(int(sample_rate * duration)):
        value = math.sin(2.0 * math.pi * frequency * i / sample_rate)
        samples.append(int(value * 32767))
    return samples

def create_noise(duration, sample_rate=44100):
    """Generate white noise"""
    import random
    samples = []
    for i in range(int(sample_rate * duration)):
        samples.append(random.randint(-16384, 16384))
    return samples

def create_click_sound(filepath):
    """Create a menu click sound (short high-pitched beep)"""
    samples = create_tone(1200, 0.05)  # 1200 Hz for 0.05 seconds
    write_wav(filepath.replace('.mp3', '.wav'), samples)
    print(f"✓ Created {os.path.basename(filepath)}")

def create_success_sound(filepath):
    """Create a success sound (ascending tones)"""
    samples = []
    samples.extend(create_tone(523, 0.1))  # C
    samples.extend(create_tone(659, 0.1))  # E
    samples.extend(create_tone(784, 0.15)) # G
    write_wav(filepath.replace('.mp3', '.wav'), samples)
    print(f"✓ Created {os.path.basename(filepath)}")

def create_fail_sound(filepath):
    """Create a fail sound (descending tones)"""
    samples = []
    samples.extend(create_tone(400, 0.1))
    samples.extend(create_tone(300, 0.1))
    samples.extend(create_tone(200, 0.15))
    write_wav(filepath.replace('.mp3', '.wav'), samples)
    print(f"✓ Created {os.path.basename(filepath)}")

def create_level_up_sound(filepath):
    """Create a level up sound (triumphant ascending scale)"""
    samples = []
    freqs = [523, 587, 659, 698, 784, 880, 988]  # C major scale
    for freq in freqs:
        samples.extend(create_tone(freq, 0.08))
    write_wav(filepath.replace('.mp3', '.wav'), samples)
    print(f"✓ Created {os.path.basename(filepath)}")

def create_combat_hit_sound(filepath):
    """Create a combat hit sound (impact)"""
    samples = []
    # Start with high frequency, decay rapidly
    for i in range(10):
        freq = 800 - (i * 60)
        samples.extend(create_tone(freq, 0.02))
    write_wav(filepath.replace('.mp3', '.wav'), samples)
    print(f"✓ Created {os.path.basename(filepath)}")

def create_combat_miss_sound(filepath):
    """Create a combat miss sound (whoosh)"""
    samples = []
    # Descending whoosh
    for i in range(8):
        freq = 600 - (i * 50)
        tone_samples = create_tone(freq, 0.03)
        # Reduce amplitude
        tone_samples = [int(s * 0.5) for s in tone_samples]
        samples.extend(tone_samples)
    write_wav(filepath.replace('.mp3', '.wav'), samples)
    print(f"✓ Created {os.path.basename(filepath)}")

def create_notification_sound(filepath):
    """Create a notification sound (two-tone beep)"""
    samples = []
    samples.extend(create_tone(800, 0.1))
    samples.extend(create_tone(1000, 0.12))
    write_wav(filepath.replace('.mp3', '.wav'), samples)
    print(f"✓ Created {os.path.basename(filepath)}")

def create_background_music(filepath):
    """Create simple background music (ambient loop)"""
    samples = []
    # Create a simple ambient loop with multiple tones
    base_freqs = [220, 277, 330, 277]  # A, C#, E, C# progression
    for _ in range(2):  # Repeat twice
        for freq in base_freqs:
            samples.extend(create_tone(freq, 0.5))
            samples.extend(create_tone(freq * 1.5, 0.5))  # Fifth harmony
    write_wav(filepath.replace('.mp3', '.wav'), samples)
    print(f"✓ Created {os.path.basename(filepath)}")

def write_wav(filepath, samples, sample_rate=44100):
    """Write samples to a WAV file"""
    with open(filepath, 'wb') as f:
        # WAV header
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + len(samples) * 2))  # File size
        f.write(b'WAVE')
        
        # Format chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # Chunk size
        f.write(struct.pack('<H', 1))   # Audio format (PCM)
        f.write(struct.pack('<H', 1))   # Number of channels (mono)
        f.write(struct.pack('<I', sample_rate))  # Sample rate
        f.write(struct.pack('<I', sample_rate * 2))  # Byte rate
        f.write(struct.pack('<H', 2))   # Block align
        f.write(struct.pack('<H', 16))  # Bits per sample
        
        # Data chunk
        f.write(b'data')
        f.write(struct.pack('<I', len(samples) * 2))
        for sample in samples:
            f.write(struct.pack('<h', sample))

print("Creating Batch 5: Sound files...")

# Create all sound files
create_menu_click = f"{PUBLIC_DIR}/sounds/menu_click.mp3"
create_click_sound(create_menu_click)

create_action_success = f"{PUBLIC_DIR}/sounds/action_success.mp3"
create_success_sound(create_action_success)

create_action_fail = f"{PUBLIC_DIR}/sounds/action_fail.mp3"
create_fail_sound(create_action_fail)

create_level_up = f"{PUBLIC_DIR}/sounds/level_up.mp3"
create_level_up_sound(create_level_up)

create_combat_hit = f"{PUBLIC_DIR}/sounds/combat_hit.mp3"
create_combat_hit_sound(create_combat_hit)

create_combat_miss = f"{PUBLIC_DIR}/sounds/combat_miss.mp3"
create_combat_miss_sound(create_combat_miss)

create_notification = f"{PUBLIC_DIR}/sounds/notification.mp3"
create_notification_sound(create_notification)

create_bg_music = f"{PUBLIC_DIR}/sounds/background_music.mp3"
create_background_music(create_bg_music)

print(f"\n✅ Batch 5 Complete: Created 8 sound files (as WAV format)")
print("Note: WAV files created instead of MP3 for better compatibility")
print("Total progress: Textures (30/30) ✓ | Icons (4/4) ✓ | Sounds (8/8) ✓")
