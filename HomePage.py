import streamlit as st
from testBG import mainn


def add_bg_from_url():
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("https://imgz.io/images/2023/07/23/image.png");
                background-attachment: fixed;
                background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
  
def main():
    # CSS for Inter font and centering
    css_code = """
    <style>
    @font-face {
        font-family: 'Inter';
        src: url('assets/fonts/Inter-Regular.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }
    
    
    
    .center {
        position:absolute;
        display:flex;
        justify-content: flex-start;
        align-items: flex-start;
        left:-250px;
        top:190px;
        width:150%
    }

    .h2-container {
        position:absolute;
        text-align: center;
    }

    .h2-text {
        font-family: 'Inter', sans-serif;
        font-size: 48px;
    }
    
    .button{
        position: absolute;
        top:350px;
    }
    </style>
    """

    # Apply CSS styling
    st.markdown(css_code, unsafe_allow_html=True)

    # Display the subheader with Inter font, centered in a column
    st.markdown("<div class='center'><div class='h2-container'><h2 class='h2-text'>ระบบสอบถามปัญหา<br>คดีอาชญากรรมทางเทคโนโลยี</h2></div></div>", unsafe_allow_html=True)


    add_bg_from_url()
    
        
    button_style = (
        "background-color: #BBDBF9; color: black; font-size: 24px; padding: 10px 50px; "
        "border: none; border-radius: 5px; cursor: pointer;"

    )
    
    # on_button_click = """
    #     <script>
    #     document.getElementById("custom-button").addEventListener("click", function() {
    #         this.style.backgroundColor = "#FF5733";
    #     });
    #     </script>
    #     """
    
    st.markdown('<button class="button" style="{}">เริ่มต้นใช้งาน</button>'.format(button_style),unsafe_allow_html=True)

    

if __name__ == '__main__':
    main()

