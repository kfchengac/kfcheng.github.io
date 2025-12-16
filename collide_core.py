from __future__ import annotations
from typing import Any, Dict, List
try:
    import plotly.graph_objects as go
except ImportError:
    go = None

class COLLIDEAdvisor:
    def __init__(self):
        self.brand_pillars = {
            "Strategic Positioning": ["Market Analysis", "Competitive Landscape", "Brand Differentiation", "Target Audience"],
            "Visual Identity": ["Brand Aesthetics", "Design Language", "Color Psychology", "Typography"],
            "Business Metrics": ["Revenue Streams", "Growth Strategy", "Financial Planning", "KPI Tracking"],
            "Authentic Vision": ["Brand Story", "Core Values", "Mission Alignment", "Purpose-Driven Strategy"],
        }

    def _calculate_positioning_score(self, d: Dict) -> float:
        return sum([d.get("market_research_complete", 0), d.get("competitor_analysis_done", 0),
                    d.get("target_audience_defined", 0), d.get("unique_value_prop_clear", 0)]) * 25

    def _calculate_visual_score(self, d: Dict) -> float:
        return sum([d.get("logo_finalized", 0), d.get("color_palette_defined", 0),
                    d.get("typography_selected", 0), d.get("brand_guidelines_created", 0),
                    d.get("visual_consistency", 0)]) * 20

    def _calculate_business_score(self, d: Dict) -> float:
        return sum([d.get("revenue_model_defined", 0), d.get("financial_projections_made", 0),
                    d.get("kpis_established", 0), d.get("growth_strategy_planned", 0)]) * 25

    def _calculate_authenticity_score(self, d: Dict) -> float:
        return sum([d.get("brand_story_developed", 0), d.get("core_values_defined", 0),
                    d.get("mission_clear", 0), d.get("purpose_aligned", 0)]) * 25

    def _determine_maturity_level(self, score: float) -> str:
        return "Evolved Brand" if score >= 80 else "Developing Brand" if score >= 60 else "Emerging Brand" if score >= 40 else "Early Stage Brand"

    def assess_brand_maturity(self, brand_data: Dict) -> Dict:
        pos = self._calculate_positioning_score(brand_data)
        vis = self._calculate_visual_score(brand_data)
        biz = self._calculate_business_score(brand_data)
        auth = self._calculate_authenticity_score(brand_data)
        overall = (pos + vis + biz + auth) / 4
        return {
            "overall_score": overall,
            "strategic_positioning": pos,
            "visual_identity": vis,
            "business_metrics": biz,
            "authenticity": auth,
            "maturity_level": self._determine_maturity_level(overall),
        }

    def _get_top_priority(self, a: Dict) -> str:
        lowest = min(
            [("strategic_positioning", a.get("strategic_positioning", 0)),
             ("visual_identity", a.get("visual_identity", 0)),
             ("business_metrics", a.get("business_metrics", 0)),
             ("authenticity", a.get("authenticity", 0))],
            key=lambda x: x[1],
        )[0]
        priorities = {
            "strategic_positioning": "Refine market positioning and competitive differentiation",
            "visual_identity": "Develop cohesive visual identity and brand guidelines",
            "business_metrics": "Establish clear KPIs and revenue optimization strategies",
            "authenticity": "Strengthen brand story and authentic value proposition",
        }
        return priorities.get(lowest, "Comprehensive brand foundation development")

    def _get_secondary_priority(self, a: Dict) -> str:
        scores = sorted([
            ("strategic_positioning", a.get("strategic_positioning", 0)),
            ("visual_identity", a.get("visual_identity", 0)),
            ("business_metrics", a.get("business_metrics", 0)),
            ("authenticity", a.get("authenticity", 0)),
        ], key=lambda x: x[1])
        priorities = {
            "strategic_positioning": "Conduct comprehensive market research and competitor analysis",
            "visual_identity": "Create consistent brand touchpoints and visual system",
            "business_metrics": "Implement tracking systems and performance dashboards",
            "authenticity": "Develop compelling brand narrative and founder story",
        }
        return priorities.get(scores[1][0], "Brand positioning optimization")

    def _get_tertiary_priority(self, a: Dict) -> str:
        scores = sorted([
            ("strategic_positioning", a.get("strategic_positioning", 0)),
            ("visual_identity", a.get("visual_identity", 0)),
            ("business_metrics", a.get("business_metrics", 0)),
            ("authenticity", a.get("authenticity", 0)),
        ], key=lambda x: x[1])
        priorities = {
            "strategic_positioning": "Build strategic partnerships and market alliances",
            "visual_identity": "Develop comprehensive brand style guide",
            "business_metrics": "Optimize pricing and revenue model",
            "authenticity": "Strengthen community engagement and brand purpose",
        }
        return priorities.get(scores[2][0], "Growth strategy development")

    def _create_executive_summary(self, assessment: Dict, client_data: Dict) -> str:
        return (
            "COLLIDE AI BRAND CONSULTATION SUMMARY\n"
            f"Brand: {client_data.get('brand_name', 'Your Brand')}\n"
            f"Industry: {client_data.get('industry', 'Creative Industry')}\n"
            f"Current Maturity Level: {assessment.get('maturity_level', '')}\n"
            f"Overall Brand Score: {assessment.get('overall_score', 0):.1f}/100\n"
            f"Immediate priorities: {self._get_top_priority(assessment)}; "
            f"{self._get_secondary_priority(assessment)}; {self._get_tertiary_priority(assessment)}"
        )

    def generate_brand_strategy(self, client_data: Dict) -> Dict:
        return {
            "brand_analysis": {"status": "placeholder"},
            "market_positioning": {"status": "placeholder"},
            "visual_direction": {"status": "placeholder"},
            "business_roadmap": {"status": "placeholder"},
            "implementation_plan": {"status": "placeholder"},
        }

    def generate_consultation_report(self, client_data: Dict) -> Dict:
        assessment = self.assess_brand_maturity(client_data)
        strategy = self.generate_brand_strategy(client_data)
        return {
            "executive_summary": self._create_executive_summary(assessment, client_data),
            "brand_assessment": assessment,
            "strategic_recommendations": strategy,
            "next_steps": ["Review assessment", "Confirm priorities", "Define 30/60/90-day plan"],
        }

    def visualize_brand_assessment(self, assessment: Dict) -> None:
        if go is None:
            print("Plotly is not installed; skipping visualization.")
            return
        categories = ["Strategic Positioning", "Visual Identity", "Business Metrics", "Authenticity"]
        values = [
            assessment.get("strategic_positioning", 0),
            assessment.get("visual_identity", 0),
            assessment.get("business_metrics", 0),
            assessment.get("authenticity", 0),
        ]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill="toself", name="Current"))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
        fig.show()

class COLLIDEConsultation:
    def __init__(self):
        self.advisor = COLLIDEAdvisor()
        self.session_data: Dict[str, Any] = {}

    def _collect_basic_info(self) -> Dict[str, Any]:
        return {
            "brand_name": "EcoLux Fashion",
            "industry": "Fashion",
            "vision": "To transform sustainable fashion into luxury experiences that inspire conscious living",
            "core_values": ["sustainability", "quality", "innovation", "transparency"],
            "brand_personality": ["sophisticated", "authentic", "innovative"],
            "target_audience": {"age_range": "25-40", "income_level": "premium", "lifestyle": "conscious consumers"},
            "current_revenue_streams": ["direct sales", "online store"],
            "market_research_complete": 1,
            "competitor_analysis_done": 0,
            "target_audience_defined": 1,
            "unique_value_prop_clear": 1,
            "logo_finalized": 0,
            "color_palette_defined": 0,
            "typography_selected": 0,
            "brand_guidelines_created": 0,
            "visual_consistency": 0,
            "revenue_model_defined": 1,
            "financial_projections_made": 0,
            "kpis_established": 0,
            "growth_strategy_planned": 0,
            "brand_story_developed": 1,
            "core_values_defined": 1,
            "mission_clear": 1,
            "purpose_aligned": 1,
            "founder_story": True,
            "social_impact_focus": True,
            "values_driven_decisions": True,
            "community_engagement": False,
        }

    def start_consultation(self) -> Dict[str, Any]:
        self.session_data = self._collect_basic_info()
        assessment = self.advisor.assess_brand_maturity(self.session_data)
        strategy = self.advisor.generate_brand_strategy(self.session_data)
        report = self.advisor.generate_consultation_report(self.session_data)
        return {"assessment": assessment, "strategy": strategy, "report": report, "session_data": self.session_data}

    def display_results(self, consultation_results: Dict[str, Any]) -> None:
        assessment = consultation_results["assessment"]
        print("COLLIDE BRAND ASSESSMENT RESULTS")
        print("=" * 50)
        print(f"Overall Brand Maturity Score: {assessment['overall_score']:.1f}/100")
        print(f"Brand Maturity Level: {assessment['maturity_level']}")
        print("\nDetailed Scores:")
        print(f"  • Strategic Positioning: {assessment['strategic_positioning']:.1f}/100")
        print(f"  • Visual Identity: {assessment['visual_identity']:.1f}/100")
        print(f"  • Business Metrics: {assessment['business_metrics']:.1f}/100")
        print(f"  • Authenticity: {assessment['authenticity']:.1f}/100")
        print("\nVisual Assessment:")
        self.advisor.visualize_brand_assessment(assessment)
        print("\n" + consultation_results["report"]["executive_summary"])

def run_collide_demo(display: bool = False) -> Dict[str, Any]:
    """Run the demo consultation and optionally print/visualize results."""
    consultation = COLLIDEConsultation()
    results = consultation.start_consultation()
    if display:
        consultation.display_results(results)
    return results
