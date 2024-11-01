## SIMPLE RECIEVE CALL
# import pyVoIP
# # Set up the SIP account
# account = pyVoIP.Account(
#     '6002',  # username
#     'mypassword',  # password
#     'localhost',  # server IP
#     5060,  # server port
#     'udp'  # transport protocol
# )

# # Set up the SIP phone
# phone = pyVoIP.Phone(account)

# # Register with the SIP server
# phone.register()

# # Wait for incoming calls
# while True:
#     call = phone.wait_for_call()
#     if call:
#         print('Received call from', call.remote_uri)
#         # Answer the call
#         call.answer()
#         # Play a welcome message
#         call.write_audio('welcome.wav')
#         # Wait for the caller to hang up
#         call.wait_for_hangup()
#         print('Call ended')
#     else:
#         print('No call received')









## PAKAI CONVERTING BYTE
# import os
# import time
# import wave
# import logging
# import numpy as np
# from pyVoIP.VoIP import VoIPPhone, CallState
# import audioop

# class VoIPRecorder:
#     def __init__(self, sample_rate=8000):
#         self.sample_rate = sample_rate
#         self.recordings_dir = os.path.join(os.getcwd(), "recordings")
#         os.makedirs(self.recordings_dir, exist_ok=True)
        
#     def process_audio_bytes(self, audio_bytes):
#         """
#         Proses byte audio dari PyVoIP dan konversi ke format yang benar
#         """
#         # Konversi bytes ke numpy array
#         audio_data = np.frombuffer(audio_bytes, dtype=np.int8)
        
#         # Normalize audio data
#         audio_data = audio_data.astype(np.float32)
#         audio_data = audio_data / np.max(np.abs(audio_data))
        
#         # Convert back to 16-bit PCM
#         audio_data = (audio_data * 32767).astype(np.int16)
        
#         return audio_data.tobytes()
    
#     def convert_to_wav(self, buffer, filename):
#         """
#         Convert buffer of audio chunks to WAV file
#         """
#         try:
#             # Concatenate all audio chunks
#             if isinstance(buffer[0], bytes):
#                 audio_data = b''.join(buffer)
#             else:
#                 audio_data = buffer

#             # Process audio data
#             processed_audio = self.process_audio_bytes(audio_data)
            
#             # Save to WAV file
#             with wave.open(filename, 'wb') as wav_file:
#                 wav_file.setnchannels(1)  # mono
#                 wav_file.setsampwidth(2)  # 16-bit
#                 wav_file.setframerate(self.sample_rate)
#                 wav_file.writeframes(processed_audio)
#             return True
            
#         except Exception as e:
#             logging.error(f"Error converting to WAV: {str(e)}")
#             return False

#     def handle_call(self, call):
#         """
#         Handle incoming calls and record audio
#         """
#         filename = f"audio_{int(time.time())}.wav"
#         tmp_filename = os.path.join(self.recordings_dir, filename)
#         buffer = []
#         total_samples = 0
        
#         try:
#             call.answer()
#             logging.info(f"Call answered from {call.call_id}")
            
#             # Process audio while call is active
#             while call.state == CallState.ANSWERED:
#                 try:
#                     # Read audio in chunks of 160 samples
#                     audio = call.read_audio(length=160, blocking=True)
                    
#                     if audio:
#                         print(audio[:20])  # Debug: print first 20 bytes
#                         buffer.append(audio)
#                         total_samples += len(audio)
                        
#                         # Save chunk when buffer reaches threshold (40000 samples)
#                         if total_samples >= 40000:
#                             print("Saving audio chunk...")
#                             if self.convert_to_wav(buffer, tmp_filename):
#                                 print(f"Saved audio chunk to {filename}")
#                                 buffer = []
#                                 total_samples = 0
#                                 # Create new filename for next chunk
#                                 tmp_filename = os.path.join(
#                                     self.recordings_dir,
#                                     f"audio_{int(time.time())}.wav"
#                                 )
                                
#                 except Exception as e:
#                     logging.error(f"Error reading audio: {str(e)}")
#                     break
                    
#             # Save any remaining audio in buffer
#             if buffer:
#                 print("Saving final audio chunk...")
#                 self.convert_to_wav(buffer, tmp_filename)
                
#         except Exception as e:
#             logging.error(f"Error during call: {str(e)}")
#         finally:
#             try:
#                 call.hangup()
#                 logging.info("Call ended")
#             except:
#                 pass

# def setup_voip_phone(sip_config):
#     """
#     Setup VoIP phone with recorder
#     """
#     recorder = VoIPRecorder()
    
#     phone = VoIPPhone(
#         sip_config['server'],
#         sip_config['port'],
#         sip_config['username'],
#         sip_config['password'],
#         callCallback=recorder.handle_call,
#         myIP=sip_config['local_ip'],
#         sipPort=sip_config['port'],
#         rtpPortLow=sip_config['rtp_port_low'],
#         rtpPortHigh=sip_config['rtp_port_high']
        
#     )
    
#     return phone, recorder



# import pyVoIP
# pyVoIP.DEBUG = False
# pyVoIP.TRANSMIT_DELAY_REDUCTION = 0.75

# def main():
#     # VoIP configuration
#     sip_config = {
#         'server': '172.27.78.87',
#         'port': 5060,
#         'username': "1001",
#         'password': "bisa1001",
#         'local_ip': "172.27.64.1",
#         'rtp_port_low': 10000,
#         'rtp_port_high': 20000
#     }
    
#     try:
#         # # Initialize VoIP client
#         # client = VoIPPhone(
#         #     sip_config['server'],
#         #     sip_config['port'],
#         #     sip_config['username'],
#         #     sip_config['password'],
#         #     callCallback=answer,
#         #     myIP=sip_config['local_ip'],
#         #     sipPort=sip_config['port'],
#         #     rtpPortLow=sip_config['rtp_port_low'],
#         #     rtpPortHigh=sip_config['rtp_port_high']
#         # )
#         client, recorder = setup_voip_phone(sip_config)
#         # Start client
#         client.start()
#         logging.info("VoIP client started. Press Ctrl+C to stop...")
        
#         # Keep running until interrupted
#         try:
#             while True:
#                 pass
#         except KeyboardInterrupt:
#             logging.info("Shutting down...")
            
#     except Exception as e:
#         logging.error(f"Error starting VoIP client: {str(e)}")
#     finally:
#         client.stop()
#         logging.info("VoIP client stopped")

# if __name__ == "__main__":
#     main()






from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState, NoPortsAvailableError
import time
import logging

# def answer(call): # This will be your callback function for when you receive a phone call.
#     try:
#       call.answer()
#       call.hangup()
#     except InvalidStateError:
#       pass
  
# if __name__ == "__main__":
#     phone=VoIPPhone('172.27.78.87', 5060, 1001, "bisa1001", callCallback=answer, myIP="0.0.0.0")
#     phone.start()
#     input('Press enter to disable the phone')
#     phone.stop()



# # Define the callback for incoming calls
# def handle_call(call):
#     try:
#         logging.info(f"Incoming call")
#         print(call.state)
#         call.answer()
#         print(call.state)
#         call.hangup()
#         print(call.state)
#     except InvalidStateError:
#         logging.error("Invalid operation based on the current state of the call.")
#     except NoPortsAvailableError:
#         logging.error("No RTP ports available.")
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")

import logging
import os
import uuid
import wave
import audioop

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
            
            # Convert audio to 16-bit if necessary (PyVoIP usually uses 16-bit)
            if len(audio_data) % 2 != 0:
                audio_data = audio_data[:-1]  # Ensure even length
            
            wav_file.writeframes(audio_data)
        
        logging.info(f"Audio saved successfully to {filename}")
        return True
    except Exception as e:
        logging.error(f"Error converting audio to WAV: {str(e)}")
        return False



def answer(call):
    """
    Handle incoming calls and record audio
    """
    tmp_dir = os.path.join(os.getcwd(), "recordings")
    os.makedirs(tmp_dir, exist_ok=True)
    filename = f"audio_{int(time.time())}.wav"
    tmp_filename = os.path.join(tmp_dir, filename)
    buffer = []
    # buffer = bytearray(b'')
    total_samples = 0
    
    try:
        call.answer()
        logging.info(f"Call answered from {call.call_id}")
        # Process audio while call is active
        while call.state == CallState.ANSWERED:
            try:
                audio = call.read_audio(length=160, blocking=True)
                # print(call.RTPClients[0].read(160, False))
                if audio:
                    print(audio[:20])
                    buffer.append(audio)
                    total_samples += len(audio)
                    if total_samples >= 40000:
                        print("A")
                        print(len(buffer))
                        if convert_to_wav(buffer, tmp_filename):
                            print(f"Saved audio chunk to {filename}")
                            buffer = []
                            total_samples = 0
                            print("B")
                            # Create new filename for next chunk
                            tmp_filename = os.path.join(tmp_dir,  f"audio_{int(time.time())}.wav")
            except Exception as e:
                logging.error(f"Error reading audio: {str(e)}")
                break
                
        # Save any remaining audio in buffer
        if buffer:
            print("C")
            convert_to_wav(buffer, tmp_filename)
            
    except Exception as e:
        logging.error(f"Error during call: {str(e)}")
    finally:
        try:
            call.hangup()
            logging.info("Call ended")
        except:
            pass


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
        # Initialize VoIP client
        client = VoIPPhone(
            sip_config['server'],
            sip_config['port'],
            sip_config['username'],
            sip_config['password'],
            callCallback=answer,
            myIP=sip_config['local_ip'],
            sipPort=sip_config['port'],
            rtpPortLow=sip_config['rtp_port_low'],
            rtpPortHigh=sip_config['rtp_port_high']
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
        client.stop()
        logging.info("VoIP client stopped")

if __name__ == "__main__":
    main()
















