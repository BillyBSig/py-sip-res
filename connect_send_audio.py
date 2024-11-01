from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import pyVoIP
import time
import wave, io
import pyaudio
import logging



# import pyaudio

# # initialize Pyaudio
# pa = pyaudio.PyAudio()

# # set parameters for audio stream
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK = 1024

# # open audio stream for recording
# stream_in = pa.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)

# # open audio stream for playback
# stream_out = pa.open(format=FORMAT,
#                      channels=CHANNELS,
#                      rate=RATE,
#                      output=True,
#                      frames_per_buffer=CHUNK)

# # record audio from microphone and play it back through speakers
# while True:
#    # read audio data from microphone
#    data = stream_in.read(CHUNK)

#    # write audio data to speakers
#    stream_out.write(data)

# # close audio streams
# stream_in.stop_stream()
# stream_out.stop_stream()
# stream_in.close()
# stream_out.close()
# pa.terminate()


import logging
import os
import uuid
import wave
import audioop
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def convert_to_wav(audio_buffer, filename):
    """
    Convert audio buffer to WAV format using the wave module
    """
    try:
        # Join all audio chunks
        audio_data = b"".join(audio_buffer)
        
        # Open WAV file for writing
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit audio
            wav_file.setframerate(8000)  # 8kHz sampling rate
            
            # Convert audio to 16-bit if necessary
            if len(audio_data) % 2 != 0:
                audio_data = audio_data[:-1]
            
            wav_file.writeframes(audio_data)
        
        logging.info(f"Audio saved successfully to {filename}")
        return True
    except Exception as e:
        logging.error(f"Error converting audio to WAV: {str(e)}")
        return False

def get_call_info(call):
    """
    Safely get call information
    """
    try:
        return {
            'from': getattr(call, 'from_uri', 'Unknown'),
            'to': getattr(call, 'to_uri', 'Unknown'),
            'call_id': getattr(call, 'call_id', str(uuid.uuid4())),
            'state': getattr(call, 'state', 'Unknown')
        }
    except Exception as e:
        logging.warning(f"Error getting call info: {str(e)}")
        return {
            'from': 'Unknown',
            'to': 'Unknown',
            'call_id': str(uuid.uuid4()),
            'state': 'Unknown'
        }

def answer(call):
    """
    Handle incoming calls and record audio
    """
    call_info = get_call_info(call)
    logging.info(f"Incoming call from: {call_info['from']} to: {call_info['to']}")
    
    # Create recordings directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tmp_dir = os.path.join(os.getcwd(), "recordings", timestamp)
    os.makedirs(tmp_dir, exist_ok=True)
    
    # Create filename with call information
    base_filename = f"call_{call_info['call_id']}"
    tmp_filename = os.path.join(tmp_dir, f"{base_filename}.wav")
    
    buffer = []
    total_samples = 0
    chunk_counter = 0
    f = wave.open(r'D:\Work\python-sip\1.wav', 'rb')
    frames = f.getnframes()
    data = f.readframes(frames)
    f.close()
    try:
        print("A")
        call.answer()
        logging.info(f"Call {call_info['call_id']} answered")
        
        call.write_audio(data)
        # Process audio while call is active
        while call.state == CallState.ANSWERED:
            print("B")
            try:
                audio = call.read_audio()
                if audio:
                    buffer.append(audio)
                    total_samples += len(audio)
                    
                    # Save every 5 seconds of audio (8000 Hz * 5 = 40000 samples)
                    if total_samples >= 40000:
                        chunk_counter += 1
                        current_filename = os.path.join(tmp_dir, f"{base_filename}_chunk{chunk_counter}.wav")
                        
                        if convert_to_wav(buffer, current_filename):
                            buffer = []
                            total_samples = 0
                            logging.info(f"Saved chunk {chunk_counter} of call {call_info['call_id']}")
                
            except Exception as e:
                logging.error(f"Error reading audio: {str(e)}")
                break
                
        # Save any remaining audio in buffer
        if buffer:
            final_filename = os.path.join(tmp_dir, f"{base_filename}_final.wav")
            convert_to_wav(buffer, final_filename)
            
    except Exception as e:
        logging.error(f"Error during call processing: {str(e)}")
    finally:
        try:
            call.hangup()
            logging.info(f"Call {call_info['call_id']} ended")
        except Exception as e:
            logging.error(f"Error hanging up call: {str(e)}")

def main():
    # VoIP configuration
    sip_config = {
        'server': '172.27.78.87',
        'port': 5060,
        'username': "1001",
        'password': "bisa1001",
        'local_ip': "172.27.64.1",
        'rtp_port_low': 10000,
        'rtp_port_high': 20000
    }
    
    
    try:
        # Initialize VoIP client with specific codec support
        client = VoIPPhone(
            sip_config['server'],
            sip_config['port'],
            sip_config['username'],
            sip_config['password'],
            callCallback=answer,
            myIP=sip_config['local_ip'],
            sipPort=sip_config['port'],
            rtpPortLow=sip_config['rtp_port_low'],
            rtpPortHigh=sip_config['rtp_port_high'],
        )
        
        # Start client
        client.start()
        logging.info("VoIP client started. Press Ctrl+C to stop...")
        
        # Keep running until interrupted
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logging.info("Shutting down...")
            
    except Exception as e:
        logging.error(f"Error starting VoIP client: {str(e)}")
    finally:
        try:
            client.stop()
            logging.info("VoIP client stopped")
        except Exception as e:
            logging.error(f"Error stopping client: {str(e)}")

if __name__ == "__main__":
    main()