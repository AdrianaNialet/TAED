import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

def main():
    st.set_page_config(layout="wide")
    
    # Custom CSS to improve visual appeal
    st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stSlider > div > div > div {
        background-color: #4e8df5;
    }
    h1, h2, h3 {
        color: #1e3d59;
    }
    .highlight {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Representació del model")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Model accuracy inputs
        st.subheader("Accuracies")
        
        # Grup predominant accuracy
        predominant_accuracy = st.slider(
            "Grup predominant Accuracy (%)",
            min_value=0.0,
            max_value=100.0,
            value=85.0,
            step=0.1,
            format="%.1f"
        )
        
        # Set a fixed value for the minority group accuracy
        minority_accuracy = st.slider(
            "Grup minoritari Accuracy (%)",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=0.1,
            format="%.1f"
        )
        
        # Weights for weighted average
        st.subheader("Distribució")
        weight1 = st.slider(
            "Pes del Grup predominant",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.01,
            format="%.2f"
        )
        weight2 = 1.0 - weight1
        
        # Calculate weighted average
        weighted_avg = (predominant_accuracy * weight1) + (minority_accuracy * weight2)
        
        # Create a compact visual display of the weights
        st.write("Distribució:")
        fig_weights = plt.figure(figsize=(6, 1))
        ax_weights = fig_weights.add_subplot(111)
        
        # Create a horizontal stacked bar
        ax_weights.barh([''], [weight1], color='#3498db', label='Grup predominant')
        ax_weights.barh([''], [weight2], left=[weight1], color='#2ecc71', label='Grup minoritari')
        
        # Add text labels
        if weight1 >= 0.15:
            ax_weights.text(weight1/2, 0, f"{weight1:.2f}", ha='center', va='center', color='white', fontsize=8, fontweight='bold')
        if weight2 >= 0.15:
            ax_weights.text(weight1 + weight2/2, 0, f"{weight2:.2f}", ha='center', va='center', color='white', fontsize=8, fontweight='bold')
        
        ax_weights.set_xlim(0, 1)
        ax_weights.set_xticks([])
        ax_weights.set_yticks([])
        ax_weights.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=8)
        ax_weights.set_frame_on(False)
        
        st.pyplot(fig_weights)
    
    with col2:
        # Results display with people representation
        st.subheader("Resultats")
        
        # Create figure for people representation
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Draw accuracy bars
        def draw_accuracy_gauge(y_pos, accuracy, label, color, height=0.5):
            # Background bar (gray)
            ax.add_patch(Rectangle((2, y_pos), 6, height, facecolor='#e0e0e0', edgecolor='none', alpha=0.5))
            # Accuracy bar
            ax.add_patch(Rectangle((2, y_pos), 6 * accuracy/100, height, facecolor=color, edgecolor='none'))
            # Label
            ax.text(1, y_pos + height/2, label, ha='right', va='center', fontsize=10, fontweight='bold')
            # Percentage
            ax.text(8.5, y_pos + height/2, f"{accuracy:.1f}%", ha='left', va='center', fontsize=10)
        
        # Draw the groups accuracy bars
        draw_accuracy_gauge(9, predominant_accuracy, "Grup predominant", '#3498db')
        draw_accuracy_gauge(8.2, minority_accuracy, "Grup minoritari", '#2ecc71')
        
        # Make the total accuracy bar bigger
        draw_accuracy_gauge(6.8, weighted_avg, "Total", '#9b59b6', height=1.2)
        
        # Draw people representation
        # Calculate number of people to draw
        total_people = 50
        predominant_people = int(round(total_people * weight1))
        minority_people = total_people - predominant_people
        
        # Calculate correct people based on accuracy
        correct_predominant = int(round(predominant_people * predominant_accuracy / 100))
        correct_minority = int(round(minority_people * minority_accuracy / 100))
        
        # Calculate positions
        people_per_row = 10
        person_width = 0.5
        person_height = 0.8
        start_x = 2
        start_y = 5
        
        # Draw predominant group people
        for i in range(predominant_people):
            row = i // people_per_row
            col = i % people_per_row
            x = start_x + col * person_width
            y = start_y - row * person_height
            
            # Person silhouette (stick figure)
            if i < correct_predominant:
                color = '#3498db'  # Blue for correct
            else:
                color = '#e74c3c'  # Red for incorrect
            
            # Draw simple stick figure
            # Head
            circle = plt.Circle((x + person_width/2, y + 0.6), 0.15, color=color)
            ax.add_patch(circle)
            # Body
            ax.plot([x + person_width/2, x + person_width/2], [y + 0.45, y + 0.2], color=color, linewidth=2)
            # Arms
            ax.plot([x + person_width/2 - 0.15, x + person_width/2 + 0.15], [y + 0.35, y + 0.35], color=color, linewidth=2)
            # Legs
            ax.plot([x + person_width/2, x + person_width/2 - 0.15], [y + 0.2, y + 0.05], color=color, linewidth=2)
            ax.plot([x + person_width/2, x + person_width/2 + 0.15], [y + 0.2, y + 0.05], color=color, linewidth=2)
        
        # Calculate starting position for minority group
        start_y_minority = start_y - ((predominant_people - 1) // people_per_row + 1) * person_height - 0.5
        
        # Draw minority group people
        for i in range(minority_people):
            row = i // people_per_row
            col = i % people_per_row
            x = start_x + col * person_width
            y = start_y_minority - row * person_height
            
            # Person silhouette
            if i < correct_minority:
                color = '#2ecc71'  # Green for correct
            else:
                color = '#e74c3c'  # Red for incorrect
            
            # Draw simple stick figure
            # Head
            circle = plt.Circle((x + person_width/2, y + 0.6), 0.15, color=color)
            ax.add_patch(circle)
            # Body
            ax.plot([x + person_width/2, x + person_width/2], [y + 0.45, y + 0.2], color=color, linewidth=2)
            # Arms
            ax.plot([x + person_width/2 - 0.15, x + person_width/2 + 0.15], [y + 0.35, y + 0.35], color=color, linewidth=2)
            # Legs
            ax.plot([x + person_width/2, x + person_width/2 - 0.15], [y + 0.2, y + 0.05], color=color, linewidth=2)
            ax.plot([x + person_width/2, x + person_width/2 + 0.15], [y + 0.2, y + 0.05], color=color, linewidth=2)
        
        # Add legend - moved lower
        predominant_patch = mpatches.Patch(color='#3498db', label='Grup predominant (correctes)')
        minority_patch = mpatches.Patch(color='#2ecc71', label='Grup minoritari (correctes)')
        incorrect_patch = mpatches.Patch(color='#e74c3c', label='Incorrectes')
        ax.legend(handles=[predominant_patch, minority_patch, incorrect_patch],
                  loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=3)
        
        # Make statistics bigger
        stats_text = (f"Grup predominant: {correct_predominant}/{predominant_people} correctes ({predominant_accuracy:.1f}%)\n"
                     f"Grup minoritari: {correct_minority}/{minority_people} correctes ({minority_accuracy:.1f}%)\n"
                     f"Total: {weighted_avg:.1f}%")
        
        # Larger stats box with bigger font
        ax.text(5, -2, stats_text, ha='center', va='center', fontsize=14, fontweight='bold',
                bbox=dict(facecolor='#f8f9fa', edgecolor='#e0e0e0', boxstyle='round,pad=0.5'))
        
        st.pyplot(fig)

if __name__ == "__main__":
    main()
