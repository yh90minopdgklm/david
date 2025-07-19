from flask import Flask, request, render_template, Response
import os, base64
from io import BytesIO
from gtts import gTTS
from werkzeug.exceptions import BadRequest
from datetime import datetime

app = Flask(__name__)

DEFAULT_LANG = os.getenv('DEFAULT_LANG', 'ko')
SUPPORTED_LANGS = ['ko', 'en', 'ja', 'es']
LOG_FILE = 'input_log.txt'

def log_input(text, lang, error=None):
    """사용자 입력을 로그 파일에 기록"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] 텍스트: {text}, 언어: {lang}"
    if error:
        log_entry += f", 에러: {str(error)}"
    
    # 파일에 로그 작성
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # 폼 데이터 유효성 검사
            text = request.form.get('input_text').strip()
            if not text:
                raise ValueError("텍스트를 입력해주세요.")
                
            lang = request.form.get('lang', DEFAULT_LANG)
            if lang not in SUPPORTED_LANGS:
                raise BadRequest(f"지원되지 않는 언어입니다. 지원되는 언어: {', '.join(SUPPORTED_LANGS)}")
                    
            # TTS 생성
            fp = BytesIO()
            tts = gTTS(text=text, lang=lang)
            tts.write_to_fp(fp)
            fp.seek(0)
            
            # 오디오 데이터 반환
            audio_base64 = base64.b64encode(fp.getvalue()).decode('utf-8')
            log_input(text, lang)
            return render_template('index.html',
                                   error=None,
                                   audio=audio_base64,
                                   download_url=f"data:audio/mpeg;base64,{audio_base64}")
        
        except ValueError as e:
            log_input(request.form.get('input_text', ''), request.form.get('lang', DEFAULT_LANG), str(e))
            return render_template('index.html', error=str(e), audio=None)
        except BadRequest as e:
            log_input(request.form.get('input_text', ''), request.form.get('lang', DEFAULT_LANG), str(e))
            return render_template('index.html', error=str(e), audio=None)
        except Exception as e:
            log_input(request.form.get('input_text', ''), request.form.get('lang', DEFAULT_LANG), str(e))
            return render_template('index.html', error="오디오 변환이 실패했습니다.", audio=None)
    else:
        return render_template('index.html', error=None, audio=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)