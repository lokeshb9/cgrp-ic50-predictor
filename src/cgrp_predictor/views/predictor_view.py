"""
Predictor Tab View
==================

Handles rendering and logic for the main IC50 prediction interface.
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PredictorView:
    """Renders the main prediction tab."""
    
    def __init__(self, config, content, predictor, data_processor, ui):
        self.config = config
        self.content = content
        self.predictor = predictor
        self.data_processor = data_processor
        self.ui = ui
        self.project_root = Path(__file__).parent.parent.parent.parent
    
    def render(self):
        """Render complete predictor tab."""
        self._render_header()
        self._render_info_sections()
        self._render_upload_section()
        self._render_example_section()
    
    def _render_header(self):
        """Render creative hero section."""
        # Title and subtitle
        st.markdown('<h1 style="text-align: center; color: #667eea; font-size: 2.8rem; margin-bottom: 0;">🧬 Predict CGRP Inhibition</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #6c757d; font-size: 1.1rem; margin-top: 0.5rem;">Get IC50 predictions in seconds • Powered by Random Forest ML</p>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Key metrics in columns - clean display without confusing arrows
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);"><div style="font-size: 2rem;">🎯</div><div style="font-weight: 700; color: #1f77b4; font-size: 1.8rem; margin: 0.5rem 0;">82%</div><div style="color: #6c757d; font-size: 0.9rem;">R² Score</div></div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);"><div style="font-size: 2rem;">🧪</div><div style="font-weight: 700; color: #1f77b4; font-size: 1.8rem; margin: 0.5rem 0;">538</div><div style="color: #6c757d; font-size: 0.9rem;">Training Compounds</div></div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);"><div style="font-size: 2rem;">⚡</div><div style="font-weight: 700; color: #1f77b4; font-size: 1.8rem; margin: 0.5rem 0;">~3s</div><div style="color: #6c757d; font-size: 0.9rem;">Per 20 molecules</div></div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div style="text-align: center; padding: 1rem; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);"><div style="font-size: 2rem;">🤖</div><div style="font-weight: 700; color: #1f77b4; font-size: 1.8rem; margin: 0.5rem 0;">RF</div><div style="color: #6c757d; font-size: 0.9rem;">Random Forest</div></div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    def _render_info_sections(self):
        """Render compact info section using native Streamlit."""
        with st.expander("ℹ️ **About & Limitations**", expanded=False):
            st.markdown("#### What this tool does:")
            st.write("Predicts IC50 values (inhibitory concentration) for small molecules against the CGRP receptor using machine learning.")
            
            st.markdown("#### ⚠️ Important Limitations:")
            st.write("""
            - Computational estimates only (not lab results)
            - Best accuracy for molecules under 2,000 Daltons  
            - Requires Java Runtime Environment installed
            """)
            
            st.markdown("#### ✓ Training Data:")
            st.write("538 validated CGRP compounds from ChEMBL database")
    
    def _render_upload_section(self):
        """Render simplified, focused upload section."""
        st.markdown("## 🚀 Get Started")
        st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # Single focused upload area
        uploaded_file = st.file_uploader(
            "**Drag and drop your CSV or TXT file here**",
            type=["csv", "txt"],
            help="Format: 2 columns (ChEMBL_ID, SMILES) with no headers",
            accept_multiple_files=False,
            label_visibility="visible"
        )
        
        if uploaded_file:
            file_ext = Path(uploaded_file.name).suffix.upper()[1:]
            file_size_kb = uploaded_file.size / 1024
            
            st.markdown(f"""
            <div style="background: linear-gradient(to right, #d4edda, #c3e6cb); 
                        padding: 1rem 1.5rem; 
                        border-radius: 10px; 
                        border-left: 5px solid #28a745; 
                        margin: 1rem 0;
                        box-shadow: 0 2px 8px rgba(40,167,69,0.2);">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2.5rem;">✅</div>
                    <div>
                        <div style="font-weight: 700; color: #155724; font-size: 1.1rem;">{uploaded_file.name}</div>
                        <div style="color: #6c757d; font-size: 0.9rem; margin-top: 0.25rem;">
                            {file_ext} format • {file_size_kb:.1f} KB • Ready to process
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            self._process_upload(uploaded_file)
    
    def _process_upload(self, uploaded_file):
        """Process uploaded file and show predictions."""
        from cgrp_predictor.fingerprint_generator import FingerprintGenerator
        
        try:
            # Read and validate
            with st.spinner(self.config.get('ui.progress_messages.reading')):
                df = pd.read_csv(uploaded_file, sep=None, engine="python", header=None)
                
                if df.shape[1] != 2:
                    self.ui.error_box(f"Expected 2 columns, found {df.shape[1]}")
                    st.info("💡 **Required format:** Column 1 = ChEMBL ID, Column 2 = SMILES")
                    st.stop()
            
            df.columns = ["ChEMBL_ID", "SMILES"]
            
            st.markdown(f"""
            <div class="success-box">
                ✅ <strong>Successfully loaded {len(df)} molecules</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Show sample
            with st.expander("👀 View Uploaded Data", expanded=True):
                display_df = df.head(10).copy()
                st.dataframe(
                    display_df,
                    column_config={
                        "ChEMBL_ID": st.column_config.TextColumn("ChEMBL ID", width="medium"),
                        "SMILES": st.column_config.TextColumn("Molecular Structure (SMILES)", width="large")
                    },
                    hide_index=True,
                    height=350
                )
            
            # Generate fingerprints and predict
            with st.spinner(self.config.get('ui.progress_messages.preparing')):
                smi_file = self.data_processor.prepare_smi_file(df, "temp_molecules.smi")
                if not smi_file:
                    raise ValueError("Failed to prepare molecular data")
            
            with st.spinner(self.config.get('ui.progress_messages.fingerprinting')):
                generator = FingerprintGenerator(timeout=self.config.get('processing.padel.timeout_seconds', 300))
                df_fingerprints = generator.generate(smi_file, "temp_fingerprints.csv")
            
            with st.spinner(self.config.get('ui.progress_messages.predicting')):
                predictions = self.predictor.predict(df_fingerprints, include_classification=True)
            
            self.ui.success_box(self.config.get('ui.progress_messages.complete'))
            
            # Display results
            self._display_results(predictions, df)
            
            # Cleanup
            self._cleanup_temp_files(["temp_molecules.smi", "temp_fingerprints.csv"])
            
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            self.ui.error_box(f"Error: {str(e)}")
            
            if "java" in str(e).lower():
                st.error("🔴 **Java is not installed!**")
                st.info("Install: `brew install openjdk` or https://www.java.com")
            
            self._cleanup_temp_files(["temp_molecules.smi", "temp_fingerprints.csv"])
    
    def _display_results(self, predictions, original_df):
        """Display prediction results."""
        st.markdown("---")
        st.subheader("📊 Prediction Results")
        
        results = pd.concat([original_df['ChEMBL_ID'].reset_index(drop=True), predictions], axis=1)
        
        # Summary statistics
        self._render_summary_stats(results)
        
        # Detailed table
        self._render_results_table(results)
        
        # Download and interpretation
        self._render_download_section(results)
        self._render_interpretation_guide()
    
    def _render_summary_stats(self, results):
        """Render summary statistics cards with visual appeal."""
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📊 Summary Statistics")
        st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4, gap="medium")
        
        total = len(results)
        active_count = len(results[results['Classification'] == 'Active'])
        intermediate_count = len(results[results['Classification'] == 'Intermediate'])
        inactive_count = len(results[results['Classification'] == 'Inactive'])
        
        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;
                        border-top: 4px solid #1f77b4;">
                <div style="color: #6c757d; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">
                    Total Analyzed
                </div>
                <div style="font-size: 2.5rem; color: #1f77b4; font-weight: 700; margin: 0.75rem 0;">
                    {total}
                </div>
                <div style="color: #6c757d; font-size: 0.9rem;">molecules</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            percentage = (active_count / total * 100) if total > 0 else 0
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        box-shadow: 0 4px 12px rgba(40,167,69,0.15); text-align: center;
                        border-top: 4px solid #28a745;">
                <div style="color: #28a745; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">
                    🟢 Active
                </div>
                <div style="font-size: 2.5rem; color: #28a745; font-weight: 700; margin: 0.75rem 0;">
                    {active_count}
                </div>
                <div style="color: #6c757d; font-size: 0.85rem;">{percentage:.1f}%</div>
                <div style="color: #999; font-size: 0.8rem; margin-top: 0.25rem;">Strong inhibitors</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            percentage = (intermediate_count / total * 100) if total > 0 else 0
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        box-shadow: 0 4px 12px rgba(255,193,7,0.15); text-align: center;
                        border-top: 4px solid #ffc107;">
                <div style="color: #d39e00; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">
                    🟡 Intermediate
                </div>
                <div style="font-size: 2.5rem; color: #d39e00; font-weight: 700; margin: 0.75rem 0;">
                    {intermediate_count}
                </div>
                <div style="color: #6c757d; font-size: 0.85rem;">{percentage:.1f}%</div>
                <div style="color: #999; font-size: 0.8rem; margin-top: 0.25rem;">Moderate activity</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            percentage = (inactive_count / total * 100) if total > 0 else 0
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; 
                        box-shadow: 0 4px 12px rgba(220,53,69,0.15); text-align: center;
                        border-top: 4px solid #dc3545;">
                <div style="color: #dc3545; font-size: 0.85rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">
                    🔴 Inactive
                </div>
                <div style="font-size: 2.5rem; color: #dc3545; font-weight: 700; margin: 0.75rem 0;">
                    {inactive_count}
                </div>
                <div style="color: #6c757d; font-size: 0.85rem;">{percentage:.1f}%</div>
                <div style="color: #999; font-size: 0.8rem; margin-top: 0.25rem;">Weak/no inhibition</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    
    def _render_results_table(self, results):
        """Render results table with proper formatting."""
        st.markdown("---")
        st.markdown("### 📋 Detailed Predictions")
        
        results_display = results.copy()
        
        def format_classification(row):
            classification = row['Classification']
            ic50 = row['Predicted IC50 (nM)']
            
            emoji_map = {'Active': '🟢', 'Intermediate': '🟡', 'Inactive': '🔴'}
            return emoji_map.get(classification, '⚪'), classification, f"{ic50:,.1f}"
        
        results_display['Status'] = results.apply(lambda row: format_classification(row)[0], axis=1)
        results_display['Activity'] = results.apply(lambda row: format_classification(row)[1], axis=1)
        results_display['IC50 Value'] = results.apply(lambda row: format_classification(row)[2], axis=1)
        
        display_cols = results_display[['ChEMBL_ID', 'Status', 'IC50 Value', 'Activity']]
        
        st.dataframe(
            display_cols,
            column_config={
                "ChEMBL_ID": st.column_config.TextColumn("Compound ID", width="large"),
                "Status": st.column_config.TextColumn("", width="small"),
                "IC50 Value": st.column_config.TextColumn("IC50 (nM)", help="Lower = stronger", width="medium"),
                "Activity": st.column_config.TextColumn("Classification", width="medium")
            },
            hide_index=True,
            height=450
        )
    
    def _render_download_section(self, results):
        """Render download section and distribution chart separately."""
        import altair as alt
        
        # Distribution chart - full width, prominent
        st.markdown("---")
        st.markdown("### 📊 Classification Distribution")
        
        total = len(results)
        active_count = len(results[results['Classification'] == 'Active'])
        intermediate_count = len(results[results['Classification'] == 'Intermediate'])
        inactive_count = len(results[results['Classification'] == 'Inactive'])
        
        # Create chart data
        chart_data = pd.DataFrame({
            'Category': ['🟢 Active', '🟡 Intermediate', '🔴 Inactive'],
            'Count': [active_count, intermediate_count, inactive_count],
            'Color': ['#28a745', '#ffc107', '#dc3545']
        })
        
        # Modern horizontal bar chart
        chart = alt.Chart(chart_data).mark_bar(cornerRadiusEnd=4).encode(
            x=alt.X('Count:Q', title='Number of Compounds', axis=alt.Axis(labelFontSize=12)),
            y=alt.Y('Category:N', title=None, sort=None, axis=alt.Axis(labelFontSize=13, labelFontWeight='bold')),
            color=alt.Color('Color:N', scale=None, legend=None),
            tooltip=[
                alt.Tooltip('Category:N', title='Classification'),
                alt.Tooltip('Count:Q', title='Count')
            ]
        ).properties(
            height=150
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            grid=False
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # Download button - centered below chart
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            csv = results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Complete Results as CSV",
                data=csv,
                file_name="cgrp_predictions.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    def _render_interpretation_guide(self):
        """Render IC50 interpretation guide using native Streamlit."""
        with st.expander("💡 **Understanding Your Results**", expanded=False):
            st.markdown("#### What is IC50?")
            st.write("**IC50 (Inhibitory Concentration 50%)** is the concentration of a compound needed to block 50% of CGRP receptor activity. Measured in **nanomolar (nM)**.")
            
            st.markdown("---")
            st.markdown("#### 📊 Classification Guide")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.success("**🟢 Active**")
                st.metric(label="Threshold", value="< 1,000 nM")
                st.caption("Strong inhibitor • High therapeutic potential")
            
            with col2:
                st.warning("**🟡 Intermediate**")
                st.metric(label="Threshold", value="1,000-10,000 nM")
                st.caption("Moderate activity • May need optimization")
            
            with col3:
                st.error("**🔴 Inactive**")
                st.metric(label="Threshold", value="> 10,000 nM")
                st.caption("Weak/no inhibition • Not viable")
            
            st.info("**🎯 Key Takeaway:** Lower IC50 = Better! A compound with 100 nM is 10x stronger than 1,000 nM. FDA-approved gepants range from 0.1-100 nM.")
    
    def _render_example_section(self):
        """Render compact example section."""
        # Minimal, collapsed by default
        with st.expander("📦 **Download Example Files**"):
            cols = st.columns(2)
            example_files = [
                ("data/example_input.csv", "example_input.csv"),
                ("data/example_input.txt", "example_input.txt")
            ]
            
            for col, (filepath, filename) in zip(cols, example_files):
                with col:
                    if Path(filepath).exists():
                        with open(filepath, "rb") as f:
                            st.download_button(
                                label=f"⬇️ {filename}",
                                data=f.read(),
                                file_name=filename,
                                mime="text/csv",
                                use_container_width=True
                            )
    
    @staticmethod
    def _cleanup_temp_files(files):
        """Clean up temporary files."""
        for file_path in files:
            try:
                if Path(file_path).exists():
                    os.remove(file_path)
                    logger.info(f"Cleaned up: {file_path}")
            except Exception as e:
                logger.warning(f"Could not remove {file_path}: {e}")

