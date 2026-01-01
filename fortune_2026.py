#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026년 운세 프로그램
생년월일과 태어난 시각을 입력받아 월별 운세를 제공합니다.
"""

import os
import json
from datetime import datetime, date
from typing import Dict, Any
from dotenv import load_dotenv
import openai

# 환경 변수 로드
load_dotenv()

class Fortune2026:
    def __init__(self):
        """운세 클래스 초기화"""
        # OpenAI API 설정
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다.")
        
        self.client = openai.OpenAI(api_key=openai.api_key)
        
        # 운세 카테고리 정의
        self.fortune_categories = [
            "건강운", "금전운", "학업/사업운", "인간관계운", 
            "연애운", "가족운", "취업/승진운", "여행운"
        ]
        
        # 월별 이름
        self.months = [
            "1월", "2월", "3월", "4월", "5월", "6월",
            "7월", "8월", "9월", "10월", "11월", "12월"
        ]

    def get_birth_info(self) -> Dict[str, Any]:
        """사용자로부터 생년월일과 태어난 시각 입력받기"""
        print("=" * 60)
        print("🔮 2026년 운세 프로그램에 오신 것을 환영합니다! 🔮")
        print("=" * 60)
        
        while True:
            try:
                # 생년월일 입력
                birth_date_str = input("\n생년월일을 입력하세요 (YYYY-MM-DD 형식, 예: 1990-05-15): ").strip()
                birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
                
                # 태어난 시각 입력
                birth_time_str = input("태어난 시각을 입력하세요 (HH:MM 형식, 24시간, 예: 14:30): ").strip()
                birth_time = datetime.strptime(birth_time_str, "%H:%M").time()
                
                # 성별 입력
                while True:
                    gender = input("성별을 입력하세요 (남/여): ").strip()
                    if gender in ['남', '여']:
                        break
                    print("올바른 성별을 입력해주세요 (남 또는 여)")
                
                birth_info = {
                    'birth_date': birth_date,
                    'birth_time': birth_time,
                    'birth_datetime_str': f"{birth_date_str} {birth_time_str}",
                    'gender': gender,
                    'age_in_2026': 2026 - birth_date.year
                }
                
                print(f"\n입력하신 정보:")
                print(f"생년월일: {birth_date}")
                print(f"태어난 시각: {birth_time}")
                print(f"성별: {gender}")
                print(f"2026년 나이: {birth_info['age_in_2026']}세")
                
                confirm = input("\n입력하신 정보가 맞습니까? (y/n): ").strip().lower()
                if confirm == 'y':
                    return birth_info
                
            except ValueError as e:
                print(f"올바른 형식으로 입력해주세요. 오류: {e}")

    def create_fortune_prompt(self, birth_info: Dict[str, Any], month: str) -> str:
        """특정 월의 운세를 위한 프롬프트 생성"""
        prompt = f"""
당신은 한국의 전통 사주명리학과 현대적 운세 해석을 전문으로 하는 운세 전문가입니다.

다음 정보를 바탕으로 2026년 {month}의 운세를 상세하게 분석해주세요:

**개인 정보:**
- 생년월일: {birth_info['birth_date']}
- 태어난 시각: {birth_info['birth_time']}
- 성별: {birth_info['gender']}
- 2026년 나이: {birth_info['age_in_2026']}세

**분석 요청 사항:**
2026년 {month}에 대해 다음 8개 영역별로 운세를 분석해주세요:

1. **건강운** (신체적, 정신적 건강 상태 및 주의사항)
2. **금전운** (수입, 지출, 투자, 재정 관리)
3. **학업/사업운** (학습능력, 사업성과, 업무효율성)
4. **인간관계운** (대인관계, 사회적 네트워킹, 갈등 해결)
5. **연애운** (기존 관계 발전, 새로운 만남, 결혼 운)
6. **가족운** (가족 간 화합, 가정사, 효도 운)
7. **취업/승진운** (직업 운세, 승진 가능성, 이직 운)
8. **여행운** (국내외 여행, 이사, 환경 변화)

**출력 형식:**
각 영역별로 다음과 같이 작성해주세요:
- 운세 점수: ★★★★☆ (5점 만점)
- 핵심 키워드: 3-5개의 키워드
- 상세 분석: 2-3문단 (구체적인 조언 포함)
- 주의사항: 피해야 할 것들
- 추천 행동: 실천하면 좋은 것들

전통적인 사주명리학 이론을 바탕으로 하되, 현대인의 라이프스타일을 고려한 실용적인 조언을 제공해주세요.
답변은 한국어로 작성하고, 따뜻하면서도 전문적인 톤을 유지해주세요.
"""
        return prompt

    def create_yearly_summary_prompt(self, birth_info: Dict[str, Any], monthly_fortunes: Dict[str, str]) -> str:
        """연간 종합 운세를 위한 프롬프트 생성"""
        prompt = f"""
당신은 한국의 전통 사주명리학과 현대적 운세 해석을 전문으로 하는 운세 전문가입니다.

다음 개인 정보와 월별 운세 분석을 바탕으로 2026년 전체 운세의 종합적인 판단을 제공해주세요:

**개인 정보:**
- 생년월일: {birth_info['birth_date']}
- 태어난 시각: {birth_info['birth_time']}
- 성별: {birth_info['gender']}
- 2026년 나이: {birth_info['age_in_2026']}세

**월별 운세 요약:**
{json.dumps(monthly_fortunes, ensure_ascii=False, indent=2)}

**종합 분석 요청:**
위의 월별 운세를 종합하여 다음 내용을 포함한 2026년 전체 운세를 제공해주세요:

1. **2026년 전체 운세 개요** (총평 및 전반적인 흐름)
2. **최고의 시기** (가장 좋은 운세를 보이는 시기와 이유)
3. **주의가 필요한 시기** (조심해야 할 시기와 대비 방법)
4. **핵심 테마** (2026년을 관통하는 주요 테마 3가지)
5. **분야별 연간 종합 점수**:
   - 건강운: ★★★★☆
   - 금전운: ★★★★☆
   - 학업/사업운: ★★★★☆
   - 인간관계운: ★★★★☆
   - 연애운: ★★★★☆
   - 가족운: ★★★★☆
   - 취업/승진운: ★★★★☆
   - 여행운: ★★★★☆

6. **2026년 핵심 조언** (실천하면 좋을 구체적인 행동 지침 5가지)
7. **행운의 요소들** (행운의 색깔, 숫자, 방향, 음식 등)
8. **마무리 격려 메시지**

전통적인 사주명리학을 바탕으로 하되, 현대적이고 실용적인 관점에서 희망적이고 건설적인 조언을 제공해주세요.
답변은 한국어로 작성하고, 따뜻하고 격려하는 톤을 유지해주세요.
"""
        return prompt

    def get_gpt_response(self, prompt: str) -> str:
        """GPT API를 통해 운세 분석 결과 받기"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # GPT-4 사용 (GPT-5.2는 아직 공개되지 않음)
                messages=[
                    {"role": "system", "content": "당신은 한국의 전통 사주명리학과 현대 운세학을 전문으로 하는 숙련된 역술가입니다. 정확하고 상세한 분석을 통해 도움이 되는 조언을 제공합니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"운세 분석 중 오류가 발생했습니다: {str(e)}"

    def generate_monthly_fortune(self, birth_info: Dict[str, Any]) -> Dict[str, str]:
        """월별 운세 생성"""
        monthly_fortunes = {}
        
        print("\n" + "=" * 60)
        print("🌟 2026년 월별 운세를 분석하고 있습니다... 🌟")
        print("=" * 60)
        
        for i, month in enumerate(self.months, 1):
            print(f"\n📅 {month} 운세 분석 중...")
            prompt = self.create_fortune_prompt(birth_info, month)
            fortune = self.get_gpt_response(prompt)
            monthly_fortunes[month] = fortune
            print(f"✅ {month} 완료 ({i}/12)")
        
        return monthly_fortunes

    def generate_yearly_summary(self, birth_info: Dict[str, Any], monthly_fortunes: Dict[str, str]) -> str:
        """연간 종합 운세 생성"""
        print("\n🔮 2026년 종합 운세를 분석하고 있습니다...")
        prompt = self.create_yearly_summary_prompt(birth_info, monthly_fortunes)
        return self.get_gpt_response(prompt)

    def save_fortune_report(self, birth_info: Dict[str, Any], monthly_fortunes: Dict[str, str], yearly_summary: str):
        """운세 보고서를 파일로 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fortune_2026_{birth_info['birth_date'].strftime('%Y%m%d')}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("🔮 2026년 개인 운세 보고서 🔮\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("📋 개인 정보\n")
            f.write("-" * 40 + "\n")
            f.write(f"생년월일: {birth_info['birth_date']}\n")
            f.write(f"태어난 시각: {birth_info['birth_time']}\n")
            f.write(f"성별: {birth_info['gender']}\n")
            f.write(f"2026년 나이: {birth_info['age_in_2026']}세\n")
            f.write(f"보고서 생성일: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}\n\n")
            
            # 월별 운세
            for month in self.months:
                f.write(f"\n{'=' * 60}\n")
                f.write(f"📅 2026년 {month} 운세\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(monthly_fortunes[month] + "\n\n")
            
            # 연간 종합
            f.write(f"\n{'=' * 80}\n")
            f.write("🌟 2026년 종합 운세\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(yearly_summary)
        
        return filename

    def display_fortune(self, monthly_fortunes: Dict[str, str], yearly_summary: str):
        """운세 결과를 화면에 출력"""
        print("\n" + "=" * 80)
        print("🔮 2026년 운세 결과 🔮")
        print("=" * 80)
        
        # 월별 운세 출력
        for month in self.months:
            print(f"\n{'=' * 60}")
            print(f"📅 2026년 {month} 운세")
            print(f"{'=' * 60}")
            print(monthly_fortunes[month])
            print("\n" + "-" * 60)
            input("다음 달 운세를 보려면 Enter를 누르세요...")
        
        # 연간 종합 운세 출력
        print(f"\n{'=' * 80}")
        print("🌟 2026년 종합 운세")
        print(f"{'=' * 80}")
        print(yearly_summary)

    def run(self):
        """메인 실행 함수"""
        try:
            # 1. 생년월일과 시각 입력받기
            birth_info = self.get_birth_info()
            
            # 2. 월별 운세 생성
            monthly_fortunes = self.generate_monthly_fortune(birth_info)
            
            # 3. 연간 종합 운세 생성
            yearly_summary = self.generate_yearly_summary(birth_info, monthly_fortunes)
            
            # 4. 결과 출력
            self.display_fortune(monthly_fortunes, yearly_summary)
            
            # 5. 파일로 저장
            filename = self.save_fortune_report(birth_info, monthly_fortunes, yearly_summary)
            
            print(f"\n{'=' * 80}")
            print("✅ 운세 분석이 완료되었습니다!")
            print(f"📄 결과가 '{filename}' 파일로 저장되었습니다.")
            print("🙏 좋은 2026년 되시길 바랍니다!")
            print("=" * 80)
            
        except KeyboardInterrupt:
            print("\n\n프로그램이 중단되었습니다.")
        except Exception as e:
            print(f"\n오류가 발생했습니다: {e}")

def main():
    """메인 함수"""
    fortune_app = Fortune2026()
    fortune_app.run()

if __name__ == "__main__":
    main()