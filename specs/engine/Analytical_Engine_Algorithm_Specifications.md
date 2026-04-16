# Analytical Engine Algorithm Specifications

MVP algorithm definitions for Layers 2-5 of the Analytical Engine. Layer 1 (Scoring) algorithms are defined in `Scoring_Algorithm_Specification.md`. This document provides the computable logic for the remaining structured layers, scoped to what Phase 3 must implement.

---

## Sources

- `Analytical_Engine_Specification.md` — Layer definitions, entity types, techniques, outputs
- `Analytical_Question_Inventory.md` — 16 diagnostic question categories for Layer 3
- `Basic_Analytic_Data_Set.md` — 124 KPIs referenced by all layers
- `BADS_Edge_Case_Rules.md` — Missing data and edge case handling
- `Service_Interface_Contracts.md` — §8 Finding Compiler, §9 Impact Engine

---

## Layer 2 — Cohort Profiling

### Algorithm: Entity Ranking and Cohort Assignment

For each of the 16 entity types defined in `Analytical_Engine_Specification.md` lines 230-246:

```
FUNCTION profile_entity_type(
    entities: LIST[Entity],
    ranking_metric: STRING,
    assessment_id: UUID
) -> CohortProfile:

    # 1. Compute the ranking metric for each entity
    ranked = []
    FOR entity IN entities:
        value = compute_metric(entity, ranking_metric, assessment_id)
        IF value IS NOT NULL:
            ranked.append((entity, value))
    
    # Skip if insufficient data
    IF len(ranked) < 3:
        RETURN CohortProfile(status="insufficient_data", min_required=3, actual=len(ranked))
    
    # 2. Sort by ranking metric (descending for higher-is-better, ascending for lower-is-better)
    ranked.sort(by=value, direction=metric_direction(ranking_metric))
    
    # 3. Assign cohorts using tercile boundaries
    n = len(ranked)
    top_cutoff = CEIL(n / 3)
    bottom_cutoff = n - CEIL(n / 3)
    
    FOR i, (entity, value) IN enumerate(ranked):
        IF i < top_cutoff:
            entity.cohort = "top"
        ELIF i >= bottom_cutoff:
            entity.cohort = "bottom"
        ELSE:
            entity.cohort = "middle"
    
    # 4. Profile each cohort — compute summary statistics across ALL available fields
    top_entities = [e for e, v in ranked if e.cohort == "top"]
    middle_entities = [e for e, v in ranked if e.cohort == "middle"]
    bottom_entities = [e for e, v in ranked if e.cohort == "bottom"]
    
    top_profile = compute_cohort_profile(top_entities, all_fields)
    middle_profile = compute_cohort_profile(middle_entities, all_fields)
    bottom_profile = compute_cohort_profile(bottom_entities, all_fields)
    
    # 5. Identify differentiators between cohorts
    differentiators = find_differentiators(top_profile, middle_profile, bottom_profile)
    
    # 6. Identify data completeness per cohort
    data_gaps = compute_data_gaps(top_entities, middle_entities, bottom_entities)
    
    RETURN CohortProfile(
        entity_type=entity_type_name,
        ranked_list=ranked,
        top=top_profile,
        middle=middle_profile,
        bottom=bottom_profile,
        differentiators=differentiators,
        data_gaps=data_gaps
    )
```

### Cohort Profile Computation

```
FUNCTION compute_cohort_profile(entities: LIST[Entity], fields: LIST[str]) -> dict:
    profile = {}
    FOR field IN fields:
        values = [get_field(e, field) for e in entities if get_field(e, field) IS NOT NULL]
        IF len(values) > 0:
            profile[field] = {
                "mean": MEAN(values),
                "median": MEDIAN(values),
                "min": MIN(values),
                "max": MAX(values),
                "count": len(values),
                "missing": len(entities) - len(values)
            }
    RETURN profile
```

### Differentiator Detection

```
FUNCTION find_differentiators(top, middle, bottom) -> LIST[Differentiator]:
    differentiators = []
    FOR field IN all_profiled_fields:
        IF field IN top AND field IN bottom:
            top_mean = top[field]["mean"]
            bottom_mean = bottom[field]["mean"]
            IF bottom_mean != 0:
                ratio = top_mean / bottom_mean
            ELSE:
                ratio = NULL
            
            # Flag as differentiator if top/bottom gap exceeds threshold
            IF ABS(top_mean - bottom_mean) > significance_threshold(field):
                differentiators.append(Differentiator(
                    field=field,
                    top_mean=top_mean,
                    bottom_mean=bottom_mean,
                    ratio=ratio,
                    direction="top_higher" if top_mean > bottom_mean else "top_lower"
                ))
    
    # Sort by absolute gap magnitude (normalized)
    differentiators.sort(by=normalized_gap, descending=True)
    RETURN differentiators
```

### MVP Entity Types (Phase 3)

Not all 16 entity types need full implementation in Phase 3. MVP cohort profiling covers:

| Priority | Entity Type | Primary Ranking Metric |
|----------|-------------|----------------------|
| 1 | Units | Total Vacant Days (lower is better) |
| 2 | Unit Types | Occupancy Rate (higher is better) |
| 3 | Leasing Agents | Lead-to-Lease % (higher is better) |
| 4 | Floor Plans | Days on Market (lower is better) |
| 5 | Traffic Sources | Cost per Lease (lower is better) |

Remaining entity types (Floors, Buildings, Deals, Concessions, Listings, Tours, Vendors, Residents, Competitors, Marketing Channels, Tech Platforms) are Phase 6 extensibility additions.

---

## Layer 3 — Correlative Diagnostics

### Algorithm: Question Answering

Each diagnostic question in the Analytical Question Inventory defines:
- The specific data fields required
- The logic to evaluate the answer
- The classification criteria (strength / weakness / neutral / data-insufficient)

```
FUNCTION answer_diagnostic_question(
    question: DiagnosticQuestion,
    data_pool: DataPool,
    assessment_id: UUID
) -> DiagnosticAnswer:

    # 1. Check data availability
    required_fields = question.required_fields
    available = {}
    missing = []
    FOR field IN required_fields:
        value = data_pool.get(field, assessment_id)
        IF value IS NOT NULL:
            available[field] = value
        ELSE:
            missing.append(field)
    
    IF len(missing) > 0 AND question.all_fields_required:
        RETURN DiagnosticAnswer(
            question_id=question.id,
            classification="data_insufficient",
            missing_fields=missing,
            confidence=0.0
        )
    
    # 2. Evaluate the question's logic
    result = question.evaluate(available)
    
    # 3. Classify the result
    classification = question.classify(result)
    # classification is one of: "strength", "weakness", "neutral", "data_insufficient"
    
    RETURN DiagnosticAnswer(
        question_id=question.id,
        classification=classification,
        result_value=result,
        fields_used=list(available.keys()),
        missing_fields=missing,
        confidence=len(available) / len(required_fields)
    )
```

### Finding Grouping

Related diagnostic answers are grouped into findings:

```
FUNCTION group_findings(answers: LIST[DiagnosticAnswer]) -> LIST[Finding]:
    # Each question has predefined group tags (e.g., "vacancy_pipeline", "pricing_strategy")
    groups = {}
    FOR answer IN answers:
        IF answer.classification IN ("strength", "weakness"):
            FOR tag IN answer.question.group_tags:
                IF tag NOT IN groups:
                    groups[tag] = Finding(tag=tag, answers=[])
                groups[tag].answers.append(answer)
    
    findings = []
    FOR tag, finding IN groups.items():
        weakness_count = COUNT(a for a in finding.answers if a.classification == "weakness")
        strength_count = COUNT(a for a in finding.answers if a.classification == "strength")
        
        finding.severity = "critical" if weakness_count >= 3 else "moderate" if weakness_count >= 2 else "minor"
        finding.net_classification = "weakness" if weakness_count > strength_count else "strength"
        findings.append(finding)
    
    RETURN sorted(findings, by=severity, descending=True)
```

### Question Evaluation Patterns

Diagnostic questions use one of these evaluation patterns:

**Threshold check:** Compare a KPI against a benchmark.
```
IF kpi_value > threshold: "strength"
ELIF kpi_value < concern_threshold: "weakness"
ELSE: "neutral"
```

**Trend check:** Compare current period to prior period.
```
IF current > prior * 1.05: "improving"
ELIF current < prior * 0.95: "declining"
ELSE: "stable"
```

**Correlation check:** Check if two fields move together.
```
correlation = PEARSON(field_a_values, field_b_values)
IF ABS(correlation) > 0.5: report correlation
```

**Comparison check:** Compare subject to comp set.
```
diff = subject_value - comp_avg
IF diff > positive_threshold: "strength"
ELIF diff < negative_threshold: "weakness"
ELSE: "neutral"
```

---

## Layer 4 — Emergent Pattern Detection

### Algorithm: Statistical Outlier Detection

```
FUNCTION detect_outliers(
    data_pool: DataPool,
    assessment_id: UUID,
    z_threshold: FLOAT = 2.0
) -> LIST[Outlier]:

    outliers = []
    
    FOR field IN numeric_fields(data_pool):
        values = data_pool.get_all_values(field, assessment_id)
        IF len(values) < 5:
            CONTINUE  # Insufficient data for outlier detection
        
        mean = MEAN(values)
        std = STDEV(values)
        IF std == 0:
            CONTINUE  # No variance
        
        FOR entity_id, value IN values:
            z_score = (value - mean) / std
            IF ABS(z_score) > z_threshold:
                outliers.append(Outlier(
                    field=field,
                    entity_id=entity_id,
                    value=value,
                    z_score=z_score,
                    mean=mean,
                    std=std,
                    direction="high" if z_score > 0 else "low"
                ))
    
    RETURN sorted(outliers, by=ABS(z_score), descending=True)
```

### Algorithm: Pareto/Concentration Analysis

```
FUNCTION detect_concentration(
    data_pool: DataPool,
    assessment_id: UUID,
    entity_type: str,
    metric: str
) -> ConcentrationResult | NULL:

    entities = data_pool.get_entities(entity_type, assessment_id)
    values = [(e.id, compute_metric(e, metric)) for e in entities]
    values = [(id, v) for id, v in values if v IS NOT NULL and v > 0]
    
    IF len(values) < 5:
        RETURN NULL
    
    total = SUM(v for _, v in values)
    values.sort(by=value, descending=True)
    
    # Find the percentage of entities responsible for N% of total
    cumulative = 0
    for i, (id, v) in enumerate(values):
        cumulative += v
        if cumulative >= total * 0.8:
            top_pct = (i + 1) / len(values) * 100
            RETURN ConcentrationResult(
                entity_type=entity_type,
                metric=metric,
                top_entity_count=i + 1,
                top_entity_pct=top_pct,
                total_entities=len(values),
                value_share=80.0,
                is_concentrated=top_pct < 30  # 30% of entities hold 80% of value
            )
    
    RETURN NULL
```

### Algorithm: Temporal Anomaly Detection

```
FUNCTION detect_temporal_anomalies(
    time_series: LIST[(DATE, FLOAT)],
    window_size: INT = 3
) -> LIST[TemporalAnomaly]:

    IF len(time_series) < window_size * 2:
        RETURN []
    
    anomalies = []
    
    FOR i FROM window_size TO len(time_series) - 1:
        recent_window = [v for _, v in time_series[i-window_size:i]]
        prior_window = [v for _, v in time_series[i-window_size*2:i-window_size]]
        
        recent_mean = MEAN(recent_window)
        prior_mean = MEAN(prior_window)
        prior_std = STDEV(prior_window)
        
        IF prior_std == 0:
            CONTINUE
        
        change_z = (recent_mean - prior_mean) / prior_std
        
        IF ABS(change_z) > 2.0:
            date = time_series[i][0]
            anomalies.append(TemporalAnomaly(
                date=date,
                metric_value=recent_mean,
                prior_mean=prior_mean,
                change_z=change_z,
                direction="spike" if change_z > 0 else "drop"
            ))
    
    RETURN anomalies
```

### MVP Scope (Phase 3)

Layer 4 MVP implements:
1. Statistical outlier detection across all numeric KPIs
2. Pareto/concentration analysis for work orders, marketing spend, vacancy
3. Temporal anomaly detection for monthly financial and occupancy trends

Advanced techniques (cluster analysis, unexpected correlation discovery, cross-entity anomaly detection) are Phase 6 extensibility additions.

---

## Layer 5 — Unified Impact Summary

### Algorithm: Finding Aggregation and Prioritization

```
FUNCTION build_impact_summary(
    layer1_scores: LIST[ScoreResult],
    layer2_profiles: LIST[CohortProfile],
    layer3_findings: LIST[Finding],
    layer4_patterns: LIST[Pattern],
    assessment_id: UUID
) -> ImpactSummary:

    # 1. Collect all findings into a unified list
    all_findings = []
    
    # From Layer 1: areas and items scoring below threshold
    FOR score IN layer1_scores:
        IF score.value < 5.0:  # Below "Concern" level
            all_findings.append(UnifiedFinding(
                source_layers=["scoring"],
                area=score.area_name,
                title=f"{score.item_name} scored {score.value:.1f}/10",
                severity=classify_score_severity(score.value),
                score_value=score.value
            ))
    
    # From Layer 2: significant cohort differentiators
    FOR profile IN layer2_profiles:
        FOR diff IN profile.differentiators[:5]:  # Top 5 per entity type
            all_findings.append(UnifiedFinding(
                source_layers=["cohort_profiling"],
                area=infer_area(diff.field),
                title=f"{profile.entity_type}: {diff.field} differs {diff.ratio:.1f}x between top and bottom",
                severity="moderate"
            ))
    
    # From Layer 3: weakness findings
    FOR finding IN layer3_findings:
        IF finding.net_classification == "weakness":
            all_findings.append(UnifiedFinding(
                source_layers=["diagnostics"],
                area=finding.primary_area,
                title=finding.summary,
                severity=finding.severity,
                diagnostic_answers=finding.answers
            ))
    
    # From Layer 4: significant patterns
    FOR pattern IN layer4_patterns:
        IF pattern.significance > 0.8:
            all_findings.append(UnifiedFinding(
                source_layers=["pattern_detection"],
                area=infer_area(pattern.primary_field),
                title=pattern.description,
                severity="moderate"
            ))
    
    # 2. Deduplicate: merge findings that address the same issue
    merged = deduplicate_findings(all_findings)
    
    # 3. Estimate financial impact for each finding
    FOR finding IN merged:
        finding.financial_impact = estimate_impact(finding, assessment_id)
    
    # 4. Prioritize by financial impact
    merged.sort(by=financial_impact.annual_value, descending=True)
    
    # 5. Assign action timeline
    FOR finding IN merged:
        IF finding.severity == "critical" AND finding.financial_impact.annual_value > 50000:
            finding.timeline = "immediate"
        ELIF finding.financial_impact.annual_value > 10000:
            finding.timeline = "short_term"
        ELSE:
            finding.timeline = "strategic"
    
    RETURN ImpactSummary(
        findings=merged,
        total_annual_impact=SUM(f.financial_impact.annual_value for f in merged),
        immediate_count=COUNT(f for f in merged if f.timeline == "immediate"),
        short_term_count=COUNT(f for f in merged if f.timeline == "short_term"),
        strategic_count=COUNT(f for f in merged if f.timeline == "strategic")
    )
```

### Finding Deduplication

```
FUNCTION deduplicate_findings(findings: LIST[UnifiedFinding]) -> LIST[UnifiedFinding]:
    # Group by area + similar title
    groups = {}
    FOR finding IN findings:
        key = (finding.area, normalize_title(finding.title))
        IF key NOT IN groups:
            groups[key] = finding
        ELSE:
            # Merge: combine source layers, take worst severity
            existing = groups[key]
            existing.source_layers = UNION(existing.source_layers, finding.source_layers)
            existing.severity = MAX_SEVERITY(existing.severity, finding.severity)
    
    RETURN list(groups.values())
```

### Financial Impact Estimation

```
FUNCTION estimate_impact(finding: UnifiedFinding, assessment_id: UUID) -> ImpactEstimate:
    # Impact estimation uses the property's actual financials and the gap identified
    
    IF finding.score_value IS NOT NULL:
        # Score-based: estimate revenue/cost impact of moving score from current to target
        gap = 7.5 - finding.score_value  # Target: "Good" threshold
        # Use area-specific impact formulas from the Simulated Optimal Budget logic
        annual_value = estimate_from_score_gap(finding.area, gap, assessment_id)
    
    ELIF finding.diagnostic_answers:
        # Diagnostic-based: use the specific KPI gaps identified
        annual_value = SUM(
            estimate_kpi_impact(answer) for answer in finding.diagnostic_answers
        )
    
    ELSE:
        # Pattern-based: estimate conservatively
        annual_value = 0  # Conservative; consultant can override
    
    RETURN ImpactEstimate(
        annual_value=annual_value,
        confidence="high" if finding.source_layers_count >= 2 else "moderate",
        methodology="score_gap" if finding.score_value else "kpi_gap"
    )
```

---

## Severity Classification

Used across all layers:

| Severity | Criteria |
|----------|---------|
| `critical` | Score < 2.5 OR annual impact > $100,000 OR safety/compliance issue |
| `moderate` | Score 2.5-5.0 OR annual impact $10,000-$100,000 |
| `minor` | Score 5.0-7.5 OR annual impact < $10,000 |

---

## Authoritative Sources

- `Analytical_Engine_Specification.md` — Layer architecture, entity types, techniques
- `Scoring_Algorithm_Specification.md` — Layer 1 algorithms (complete)
- `Analytical_Question_Inventory.md` — Layer 3 question definitions
- `Service_Interface_Contracts.md` — §6 Metric Engine, §7 Scoring Engine, §8 Finding Compiler, §9 Impact Engine

---

## Service Mapping Note

The Analytical Engine Specification defines 5 structured layers. The Service Interface Contracts define 4 Phase 3 services. The mapping is:

| Layer | Service | Notes |
|-------|---------|-------|
| Layer 1 — Scoring | Scoring Engine (§7) | Fully specified in `Scoring_Algorithm_Specification.md` |
| Layer 2 — Cohort Profiling | No dedicated service | Algorithms in this document; implementation lives within the Finding Compiler or as a separate internal module. No service contract exists for cohort profiling as a standalone service. |
| Layer 3 — Correlative Diagnostics | Finding Compiler (§8) | 7 domain packages + contradiction engine |
| Layer 4 — Emergent Pattern Detection | No dedicated service | Algorithms in this document; implementation lives within the Finding Compiler or as a separate internal module. No service contract exists for pattern detection as a standalone service. |
| Layer 5 — Unified Impact Summary | Impact Engine (§9) | `estimate_impacts`, `get_impact_summary`, `simulate_optimal_budget` |

This gap means **Phase 3 implementation tasks do not include Layers 2 or 4 as separate deliverables**. The algorithms are defined here so they can be scoped into future tasks or folded into the Finding Compiler service when Phase 3 implementation begins.
