"""
Export and Reporting functionality for Option Pricing Calculator.
Supports CSV, Excel, and PDF exports.
"""

import pandas as pd
import io
from typing import Dict, Any, List, Optional
from datetime import datetime
import streamlit as st


class OptionReportGenerator:
    """Generate reports for option pricing calculations."""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def create_pricing_summary(
        self,
        params: Dict[str, Any],
        price: float,
        greeks: Dict[str, float],
        model_name: str
    ) -> pd.DataFrame:
        """
        Create a summary DataFrame of pricing results.
        
        Args:
            params: Input parameters
            price: Calculated option price
            greeks: Calculated Greeks
            model_name: Name of pricing model
            
        Returns:
            DataFrame with pricing summary
        """
        data = {
            'Parameter': [
                'Model',
                'Option Type',
                'Spot Price',
                'Strike Price',
                'Time to Maturity (years)',
                'Risk-Free Rate (%)',
                'Volatility (%)',
                '',  # Separator
                'Option Price',
                'Delta',
                'Gamma',
                'Theta',
                'Vega',
                'Rho',
                '',  # Separator
                'Calculation Time',
            ],
            'Value': [
                model_name,
                params['option_type'].upper(),
                f"${params['spot']:.2f}",
                f"${params['strike']:.2f}",
                f"{params['time_to_maturity']:.4f}",
                f"{params['risk_free_rate']*100:.2f}%",
                f"{params['volatility']*100:.2f}%",
                '',
                f"${price:.6f}",
                f"{greeks.get('Delta', 0):.6f}",
                f"{greeks.get('Gamma', 0):.6f}",
                f"{greeks.get('Theta', 0):.6f}",
                f"{greeks.get('Vega', 0):.6f}",
                f"{greeks.get('Rho', 0):.6f}",
                '',
                self.timestamp,
            ]
        }
        
        return pd.DataFrame(data)
    
    def create_greeks_table(self, greeks: Dict[str, float]) -> pd.DataFrame:
        """
        Create a DataFrame of Greeks.
        
        Args:
            greeks: Dictionary of Greek values
            
        Returns:
            DataFrame with Greeks
        """
        data = {
            'Greek': list(greeks.keys()),
            'Value': [f"{v:.6f}" for v in greeks.values()],
            'Description': [
                'Rate of change with respect to spot price',
                'Rate of change of Delta',
                'Time decay per day',
                'Sensitivity to volatility',
                'Sensitivity to interest rate'
            ]
        }
        
        return pd.DataFrame(data)
    
    def create_sensitivity_data(
        self,
        spot_range: List[float],
        vol_range: List[float],
        prices_vs_spot: List[float],
        prices_vs_vol: List[float]
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Create sensitivity analysis data.
        
        Args:
            spot_range: Range of spot prices
            vol_range: Range of volatilities
            prices_vs_spot: Prices at different spots
            prices_vs_vol: Prices at different vols
            
        Returns:
            DataFrame with sensitivity data
        """
        # Spot sensitivity
        spot_df = pd.DataFrame({
            'Spot Price': spot_range,
            'Option Price': prices_vs_spot
        })
        
        # Vol sensitivity
        vol_df = pd.DataFrame({
            'Volatility': [f"{v*100:.1f}%" for v in vol_range],
            'Option Price': prices_vs_vol
        })
        
        return spot_df, vol_df
    
    def export_to_csv(self, df: pd.DataFrame, include_timestamp: bool = True) -> str:
        """
        Export DataFrame to CSV string.
        
        Args:
            df: DataFrame to export
            include_timestamp: Whether to include timestamp in header
            
        Returns:
            CSV string
        """
        output = io.StringIO()
        
        if include_timestamp:
            output.write(f"# Option Pricing Calculator Report\n")
            output.write(f"# Generated: {self.timestamp}\n")
            output.write(f"#\n")
        
        df.to_csv(output, index=False)
        return output.getvalue()
    
    def export_to_excel(
        self,
        data_dict: Dict[str, pd.DataFrame],
        filename: str = "option_pricing_report.xlsx"
    ) -> bytes:
        """
        Export multiple DataFrames to Excel with different sheets.
        
        Args:
            data_dict: Dictionary mapping sheet names to DataFrames
            filename: Output filename
            
        Returns:
            Excel file as bytes
        """
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return output.getvalue()
    
    def create_full_report(
        self,
        params: Dict[str, Any],
        price: float,
        greeks: Dict[str, float],
        model_name: str,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Create a complete report with all data.
        
        Args:
            params: Input parameters
            price: Option price
            greeks: Greeks dictionary
            model_name: Model name
            additional_data: Optional additional data
            
        Returns:
            Dictionary of DataFrames for each section
        """
        report = {
            'Summary': self.create_pricing_summary(params, price, greeks, model_name),
            'Greeks': self.create_greeks_table(greeks),
        }
        
        if additional_data:
            for key, value in additional_data.items():
                if isinstance(value, pd.DataFrame):
                    report[key] = value
        
        return report


def create_download_section(
    params: Dict[str, Any],
    price: float,
    greeks: Dict[str, float],
    model_name: str
):
    """
    Create a download section in Streamlit with export options.
    
    Args:
        params: Input parameters
        price: Option price
        greeks: Greeks dictionary
        model_name: Model name
    """
    st.markdown("---")
    st.subheader("📥 Export Results")
    
    col1, col2, col3 = st.columns(3)
    
    # Initialize report generator
    generator = OptionReportGenerator()
    
    with col1:
        # CSV Export - Summary
        summary_df = generator.create_pricing_summary(params, price, greeks, model_name)
        csv_data = generator.export_to_csv(summary_df)
        
        st.download_button(
            label="📄 Download Summary (CSV)",
            data=csv_data,
            file_name=f"option_pricing_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download pricing summary as CSV file"
        )
    
    with col2:
        # CSV Export - Greeks
        greeks_df = generator.create_greeks_table(greeks)
        greeks_csv = generator.export_to_csv(greeks_df)
        
        st.download_button(
            label="📊 Download Greeks (CSV)",
            data=greeks_csv,
            file_name=f"option_greeks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download Greeks values as CSV file"
        )
    
    with col3:
        # Excel Export - Full Report
        try:
            report_data = generator.create_full_report(params, price, greeks, model_name)
            excel_data = generator.export_to_excel(
                report_data,
                f"option_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
            
            st.download_button(
                label="📑 Download Full Report (Excel)",
                data=excel_data,
                file_name=f"option_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download complete report as Excel file with multiple sheets"
            )
        except ImportError:
            st.info("Install openpyxl for Excel export: pip install openpyxl")


def create_batch_export_section(results_list: List[Dict[str, Any]]):
    """
    Create export section for batch calculations.
    
    Args:
        results_list: List of calculation results
    """
    if not results_list:
        st.warning("No results to export")
        return
    
    st.markdown("---")
    st.subheader("📥 Export Batch Results")
    
    # Create DataFrame from results
    df = pd.DataFrame(results_list)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV Export
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download Batch Results (CSV)",
            data=csv,
            file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download all batch results as CSV"
        )
    
    with col2:
        # Excel Export
        try:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Batch Results', index=False)
            
            st.download_button(
                label="📑 Download Batch Results (Excel)",
                data=output.getvalue(),
                file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download all batch results as Excel file"
            )
        except ImportError:
            st.info("Install openpyxl for Excel export: pip install openpyxl")


def create_heatmap_export(heatmap_data: Dict[str, Any], title: str):
    """
    Create export button for heatmap data.
    
    Args:
        heatmap_data: Dictionary containing heatmap data
        title: Title for the export
    """
    if not heatmap_data:
        return
    
    # Convert heatmap to DataFrame
    df = pd.DataFrame(
        heatmap_data.get('z', []),
        index=heatmap_data.get('y', []),
        columns=heatmap_data.get('x', [])
    )
    
    csv = df.to_csv()
    
    st.download_button(
        label=f"📥 Export {title} Data (CSV)",
        data=csv,
        file_name=f"{title.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help=f"Download {title} heatmap data as CSV"
    )
