import React from "react";
import {
  AbsoluteFill, Audio, Img, Series, interpolate, spring,
  staticFile, useCurrentFrame, useVideoConfig,
} from "remotion";
import { C, MONO, SANS } from "./theme";

/* ---------- scene durations (30 fps) ---------- */
const D = {
  hook: 330, problem: 480, solution: 450, copilot: 760,
  committee: 990, optimizer: 360, amd: 690, business: 360, close: 390,
};
export const TOTAL_FRAMES = Object.values(D).reduce((a, b) => a + b, 0);

/* ---------- helpers ---------- */
const Fill: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ background: C.ground, fontFamily: SANS, color: C.ink, padding: "90px 110px" }}>
    {children}
  </AbsoluteFill>
);

const useUp = (delay: number, dur = 22) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [delay, delay + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return { opacity: t, transform: `translateY(${(1 - t) * 26}px)` };
};

const FadeUp: React.FC<{ delay: number; children: React.ReactNode; style?: React.CSSProperties }> =
  ({ delay, children, style }) => <div style={{ ...useUp(delay), ...style }}>{children}</div>;

const Kick: React.FC<{ delay?: number; children: React.ReactNode }> = ({ delay = 0, children }) => (
  <FadeUp delay={delay} style={{
    fontFamily: MONO, fontSize: 26, letterSpacing: "0.16em", textTransform: "uppercase",
    color: C.amber, marginBottom: 34,
  }}>{children}</FadeUp>
);

const Water: React.FC = () => (
  <div style={{
    position: "absolute", left: 110, right: 110, bottom: 44, display: "flex",
    justifyContent: "space-between", fontFamily: MONO, fontSize: 22, color: C.faint,
    borderTop: `1px solid ${C.line}`, paddingTop: 22,
  }}>
    <span><b style={{ color: C.dim }}>MixMind</b> — a plant-private concrete-mix AI on AMD</span>
    <span style={{ color: C.amber }}>hellotravisss.github.io/mixmind/web</span>
  </div>
);

const Chip: React.FC<{ hot?: boolean; children: React.ReactNode }> = ({ hot, children }) => (
  <span style={{
    fontFamily: MONO, fontSize: 22, color: hot ? C.amber : C.dim,
    border: `1.5px solid ${hot ? "rgba(233,161,60,.55)" : C.line}`,
    borderRadius: 100, padding: "12px 22px", whiteSpace: "nowrap",
  }}>{children}</span>
);

const Type: React.FC<{ text: string; start: number; cps?: number; style?: React.CSSProperties }> =
  ({ text, start, cps = 1.1, style }) => {
    const f = useCurrentFrame();
    const n = Math.max(0, Math.floor((f - start) * cps));
    const shown = text.slice(0, n);
    return <span style={style}>{shown}{n > 0 && n < text.length ? "▌" : ""}</span>;
  };

const Stamp: React.FC<{ delay: number; color: string; children: React.ReactNode }> = ({ delay, color, children }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f - delay, fps, config: { damping: 11, stiffness: 190 } });
  const scale = interpolate(s, [0, 1], [2.6, 1]);
  return (
    <div style={{
      display: "inline-block", opacity: f < delay ? 0 : 1,
      transform: `scale(${scale}) rotate(-2.5deg)`,
      fontFamily: MONO, fontWeight: 700, fontSize: 44, letterSpacing: "0.05em",
      color, border: `5px solid ${color}`, borderRadius: 10, padding: "18px 30px",
    }}>{children}</div>
  );
};

/* =============== SCENES =============== */

const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const dim = interpolate(f, [D.hook - 20, D.hook], [1, 0], { extrapolateLeft: "clamp" });
  return (
    <Fill>
      <Audio src={staticFile("vo/hook.mp3")} />
      <div style={{ opacity: dim, height: "100%", display: "flex", flexDirection: "column", justifyContent: "center" }}>
        <Kick delay={6}>AMD Developer Hackathon · ACT II · Track 3 Unicorn</Kick>
        <FadeUp delay={20} style={{ fontSize: 118, fontWeight: 800, lineHeight: 1.02, letterSpacing: "-0.03em", maxWidth: 1500 }}>
          The AI committee <span style={{ color: C.amber }}>rejected</span> the cheapest, greenest mix.
        </FadeUp>
        <FadeUp delay={110} style={{ fontSize: 44, color: C.dim, marginTop: 44, maxWidth: 1250, lineHeight: 1.4 }}>
          Because the bricks would have failed on the factory floor.
        </FadeUp>
        <FadeUp delay={170} style={{ fontSize: 44, marginTop: 18, fontWeight: 600 }}>
          That judgment is <span style={{ color: C.amber }}>MixMind</span>.
        </FadeUp>
      </div>
      <Water />
    </Fill>
  );
};

const Problem: React.FC = () => (
  <Fill>
      <Audio src={staticFile("vo/problem.mp3")} />
    <div style={{ height: "100%", display: "flex", flexDirection: "column", justifyContent: "center" }}>
      <Kick delay={4}>The problem</Kick>
      <FadeUp delay={16} style={{ fontSize: 150, fontWeight: 800, letterSpacing: "-0.03em" }}>
        Concrete <span style={{ color: C.amber }}>≈ 8%</span> of global CO₂.
      </FadeUp>
      <FadeUp delay={120} style={{ fontSize: 52, color: C.dim, marginTop: 50, maxWidth: 1400, lineHeight: 1.35 }}>
        The know-how to fix a mix sits in labs <b style={{ color: C.ink }}>most plants can't afford</b>.
      </FadeUp>
      <FadeUp delay={250} style={{ fontSize: 52, marginTop: 30, maxWidth: 1400, lineHeight: 1.35, color: C.dim }}>
        And no plant will upload its recipes to a third-party AI —
        <b style={{ color: C.ink }}> the mix design is the business.</b>
      </FadeUp>
    </div>
    <Water />
  </Fill>
);

const Solution: React.FC = () => (
  <Fill>
      <Audio src={staticFile("vo/solution.mp3")} />
    <Img src={staticFile("paver-render.png")} style={{
      position: "absolute", right: 0, top: 0, height: "100%", opacity: 0.9,
      WebkitMaskImage: "linear-gradient(90deg,transparent 0%,#000 45%)",
      maskImage: "linear-gradient(90deg,transparent 0%,#000 45%)",
    }} />
    <div style={{ position: "relative", height: "100%", display: "flex", flexDirection: "column", justifyContent: "center", maxWidth: 1050 }}>
      <Kick delay={4}>MixMind</Kick>
      <FadeUp delay={16} style={{ fontSize: 92, fontWeight: 800, lineHeight: 1.05, letterSpacing: "-0.025em" }}>
        A plant's R&D department, self-hosted on <span style={{ color: C.amber }}>its own AMD GPU</span>.
      </FadeUp>
      <FadeUp delay={120} style={{ marginTop: 60, display: "flex", gap: 18, flexWrap: "wrap" }}>
        <Chip>Floor Copilot · cited answers</Chip>
        <Chip>Mix Committee · 4 agents</Chip>
      </FadeUp>
      <FadeUp delay={170} style={{ marginTop: 26, display: "flex", gap: 18, flexWrap: "wrap" }}>
        <Chip>Gemma 4 12B · LoRA fine-tuned</Chip>
        <Chip hot>The recipe never leaves the building</Chip>
      </FadeUp>
    </div>
    <Water />
  </Fill>
);

const Copilot: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Fill>
      <Audio src={staticFile("vo/copilot.mp3")} />
      <Kick delay={4}>01 · Floor Copilot — ask the floor</Kick>
      <div style={{ display: "flex", flexDirection: "column", gap: 30, marginTop: 10 }}>
        {/* question 1 */}
        <div style={{ fontFamily: MONO, fontSize: 36, color: C.dim, borderLeft: `4px solid ${C.amber}`, paddingLeft: 26 }}>
          <Type text="The press sounds like a motorcycle during main vibration." start={20} />
        </div>
        {/* answer 1 */}
        <FadeUp delay={135} style={{
          background: C.panel, border: `1px solid ${C.line}`, borderRadius: 14, padding: "36px 42px",
          fontSize: 37, lineHeight: 1.55, maxWidth: 1560,
        }}>
          The board or mold is <b>lifting off the vibrating table</b> — compaction suffers. Tune until it's an
          almost continuous high-pitched hum: twice the impacts, much better compaction.{" "}
          <span style={{ fontFamily: MONO, fontSize: 30, color: C.amber, border: "1.5px solid rgba(233,161,60,.6)", borderRadius: 6, padding: "2px 12px" }}>KB-13</span>
        </FadeUp>
        <FadeUp delay={330} style={{ fontSize: 32, color: C.faint, fontFamily: MONO }}>
          — shop-floor knowledge no generic AI has. Answered from this plant's own notes, with the source cited.
        </FadeUp>
        {/* question 2 */}
        {f > 430 && (
          <>
            <div style={{ fontFamily: MONO, fontSize: 36, color: C.dim, borderLeft: `4px solid ${C.warn}`, paddingLeft: 26 }}>
              <Type text="What is the market price of grey cement?" start={450} />
            </div>
            <FadeUp delay={545} style={{
              background: C.panel, border: `1px solid ${C.line}`, borderRadius: 14, padding: "36px 42px",
              fontSize: 37, color: C.dim, maxWidth: 1200,
            }}>
              I don't have a note on that. <span style={{ color: C.warn }}>— no notes, no guess.</span>
            </FadeUp>
          </>
        )}
        <FadeUp delay={700} style={{ display: "flex", gap: 18, marginTop: 8 }}>
          <Chip hot>100% grounded citations — 9/9 held-out</Chip>
          <Chip>0 invented answers</Chip>
        </FadeUp>
      </div>
      <Water />
    </Fill>
  );
};

const Row: React.FC<{ delay: number; cells: (string | React.ReactNode)[]; colors?: (string | undefined)[] }> =
  ({ delay, cells, colors = [] }) => (
    <FadeUp delay={delay} style={{
      display: "grid", gridTemplateColumns: "430px 220px 300px 220px 200px 1fr",
      borderBottom: `1px solid ${C.line}`, padding: "24px 0", fontSize: 34, alignItems: "baseline",
    }}>
      {cells.map((c, i) => (
        <span key={i} style={{ fontFamily: i === 0 ? SANS : MONO, color: colors[i] ?? C.ink }}>{c}</span>
      ))}
    </FadeUp>
  );

const Committee: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Fill>
      <Audio src={staticFile("vo/committee.mp3")} />
      <Kick delay={4}>02 · Mix Committee — four specialists, real numbers</Kick>
      <FadeUp delay={14} style={{ fontSize: 58, fontWeight: 800, letterSpacing: "-0.02em", marginBottom: 40 }}>
        Strength from a model trained on 1,030 real lab tests — <span style={{ color: C.amber }}>R² = 0.910</span>
      </FadeUp>
      <Row delay={60} colors={[C.faint, C.faint, C.faint, C.faint, C.faint, C.faint]}
        cells={["PROPOSED CHANGE", "28-DAY", "2-DAY ≥ 12", "COST", "CO₂", "VERDICT"]} />
      <Row delay={95} colors={[undefined, undefined, C.good, undefined, C.good, C.good]}
        cells={["Sweet spot", "52.6", "16.1 ✓", "$87.9", "−17%", "APPROVED"]} />
      <Row delay={140} colors={[undefined, undefined, C.warn, undefined, C.good, C.warn]}
        cells={["20% cement → slag", "46.3", "12.7 ✓ tight", "$88.2", "−18%", "CONDITIONS"]} />
      <Row delay={185} colors={[undefined, undefined, C.bad, undefined, C.good, C.bad]}
        cells={["Aggressive · 45% slag", "36.0", "8.0 ✗", "$84.8", "−40%", "REJECTED"]} />
      {f > 300 && (
        <div style={{ marginTop: 70, display: "flex", alignItems: "center", gap: 60 }}>
          <Stamp delay={310} color={C.bad}>REJECTED</Stamp>
          <FadeUp delay={340} style={{ fontSize: 44, lineHeight: 1.4, maxWidth: 1150 }}>
            The cheapest, greenest mix on the board — killed by QC.
            <div style={{ color: C.dim, fontSize: 36, marginTop: 14 }}>
              2-day strength 8.0 MPa fails the demould spec. The model learned slag's early-strength
              penalty <b style={{ color: C.ink }}>from the data</b> — nobody hard-coded that rule.
            </div>
          </FadeUp>
        </div>
      )}
      <FadeUp delay={640} style={{ marginTop: 60, fontSize: 52, fontWeight: 700, color: C.amber }}>
        Judgment — not a yes-man.
      </FadeUp>
      <Water />
    </Fill>
  );
};

const Optimizer: React.FC = () => {
  const f = useCurrentFrame();
  const cement = Math.round(interpolate(f, [60, 240], [320, 176], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const s2 = (interpolate(f, [60, 240], [15.7, 8.9], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })).toFixed(1);
  const fail = Number(s2) < 12;
  return (
    <Fill>
      <Audio src={staticFile("vo/optimizer.mp3")} />
      <Kick delay={4}>03 · Drive the mix — live, on the real model</Kick>
      <FadeUp delay={14} style={{ fontSize: 64, fontWeight: 800, marginBottom: 60 }}>
        Pull the cement down. Watch the verdict react.
      </FadeUp>
      <div style={{ maxWidth: 1300 }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 38, marginBottom: 18 }}>
          <span>Cement</span>
          <span style={{ fontFamily: MONO, color: C.amber }}>{cement} kg/m³</span>
        </div>
        <div style={{ height: 14, borderRadius: 8, background: C.line, position: "relative" }}>
          <div style={{
            position: "absolute", left: 0, top: 0, bottom: 0, borderRadius: 8,
            width: `${((cement - 150) / (340 - 150)) * 100}%`, background: C.amber,
          }} />
        </div>
        <div style={{ display: "flex", gap: 26, marginTop: 56, alignItems: "center" }}>
          <div style={{ fontFamily: MONO, fontSize: 46 }}>
            2-day <b style={{ color: fail ? C.bad : C.good }}>{s2} MPa</b>
            <span style={{ color: C.faint, fontSize: 32 }}>  · spec ≥ 12</span>
          </div>
          {fail && <Stamp delay={0} color={C.bad}>REJECTED</Stamp>}
          {!fail && f > 40 && <Stamp delay={40} color={C.good}>APPROVED</Stamp>}
        </div>
        <FadeUp delay={280} style={{ marginTop: 56, fontSize: 34, color: C.dim, fontFamily: MONO }}>
          Every number interpolated from the R²=0.91 model — no slideware. Try it yourself at the live URL below.
        </FadeUp>
      </div>
      <Water />
    </Fill>
  );
};

const GpuCard: React.FC<{ delay: number; title: string; tag: string; lines: string[] }> =
  ({ delay, title, tag, lines }) => (
    <FadeUp delay={delay} style={{
      background: C.panel, border: `1px solid ${C.line}`, borderRadius: 14, padding: "40px 44px", flex: 1,
    }}>
      <div style={{ fontSize: 40, fontWeight: 700 }}>{title}
        <span style={{ fontFamily: MONO, fontSize: 24, color: C.faint, border: `1px solid ${C.line}`, borderRadius: 6, padding: "4px 12px", marginLeft: 18 }}>{tag}</span>
      </div>
      <div style={{ fontFamily: MONO, fontSize: 27, color: C.dim, marginTop: 26, lineHeight: 1.8 }}>
        {lines.map((l, i) => <div key={i}>{l}</div>)}
      </div>
    </FadeUp>
  );

const Amd: React.FC = () => {
  const f = useCurrentFrame();
  const loss = interpolate(f, [300, 420], [3.029, 0.001], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Fill>
      <Audio src={staticFile("vo/amd.mp3")} />
      <Kick delay={4}>Why AMD — verified on real hardware</Kick>
      <FadeUp delay={14} style={{ fontSize: 62, fontWeight: 800, marginBottom: 50, letterSpacing: "-0.02em" }}>
        Everyone proves AMD goes <span style={{ color: C.steel }}>big</span>. We prove it goes{" "}
        <span style={{ color: C.amber }}>small enough to afford</span>.
      </FadeUp>
      <div style={{ display: "flex", gap: 26 }}>
        <GpuCard delay={70} title="Radeon PRO W7900" tag="~$4k · in the plant" lines={[
          "GPU[0] Card Vendor: Advanced Micro",
          "Devices, Inc. [AMD/ATI] · gfx1100",
          "VRAM Total: 51,522,830,336 B",
        ]} />
        <GpuCard delay={120} title="Instinct MI300X" tag="$1.99/hr · for training" lines={[
          "GPU[0] Card Series: AMD Instinct",
          "MI300X VF · gfx942",
          "VRAM Total: 205,822,885,888 B",
        ]} />
      </div>
      {f > 280 && (
        <div style={{ marginTop: 56, display: "flex", alignItems: "center", gap: 50 }}>
          <div style={{ fontFamily: MONO, fontSize: 52 }}>
            training loss <b style={{ color: C.amber }}>{loss.toFixed(3)}</b>
          </div>
          <FadeUp delay={430} style={{ fontFamily: MONO, fontSize: 34, color: C.dim }}>
            LoRA fine-tune · 60 steps · under a minute on MI300X → 287 MB adapter ships back to the plant card
          </FadeUp>
        </div>
      )}
      <FadeUp delay={520} style={{ marginTop: 50, display: "flex", gap: 18 }}>
        <Chip>ROCm 7.2 · PyTorch · PEFT</Chip>
        <Chip>Fireworks AI — independent blind judge</Chip>
        <Chip hot>evidence logs in the repo</Chip>
      </FadeUp>
      <Water />
    </Fill>
  );
};

const Business: React.FC = () => (
  <Fill>
      <Audio src={staticFile("vo/business.mp3")} />
    <div style={{ height: "100%", display: "flex", flexDirection: "column", justifyContent: "center" }}>
      <Kick delay={4}>The business — bottom-up</Kick>
      <FadeUp delay={16} style={{ fontSize: 68, fontWeight: 800, maxWidth: 1500, letterSpacing: "-0.02em", lineHeight: 1.1 }}>
        A mid-size plant spends <span style={{ color: C.amber }}>~$1M+ a year</span> on cement.
      </FadeUp>
      <div style={{ marginTop: 60, fontSize: 44, lineHeight: 2.0, fontFamily: MONO }}>
        <FadeUp delay={110}>cut 5–19% of it → <b style={{ color: C.good }}>$50K–250K saved / plant-yr</b></FadeUp>
        <FadeUp delay={170}>MixMind at $2K/mo → <b style={{ color: C.amber }}>&lt;20% of the savings</b> — pays back in month one</FadeUp>
        <FadeUp delay={230}>~3,000 N.A. plants → <b>$0.3–0.8B/yr</b> recoverable wedge</FadeUp>
      </div>
    </div>
    <Water />
  </Fill>
);

const Close: React.FC = () => (
  <Fill>
      <Audio src={staticFile("vo/close.mp3")} />
    <div style={{ height: "100%", display: "flex", flexDirection: "column", justifyContent: "center" }}>
      <div style={{ display: "flex", gap: 2, border: `1px solid ${C.line}`, borderRadius: 10, overflow: "hidden", marginBottom: 70 }}>
        {[["−17%", "CO₂, strength held", C.good], ["R² 0.910", "1,030 lab tests", C.amber],
          ["100%", "grounded citations", C.good], ["0 bytes", "sent off-site", C.steel]].map(([n, l, col], i) => (
          <FadeUp key={i} delay={10 + i * 26} style={{ flex: 1, background: C.panel, padding: "38px 34px" }}>
            <div style={{ fontFamily: MONO, fontSize: 56, fontWeight: 600, color: col as string }}>{n}</div>
            <div style={{ fontSize: 26, color: C.dim, marginTop: 10 }}>{l}</div>
          </FadeUp>
        ))}
      </div>
      <FadeUp delay={130} style={{ fontSize: 74, fontWeight: 800, letterSpacing: "-0.025em", lineHeight: 1.12 }}>
        White cement, grey cement, slag, chips —{" "}
        <span style={{ color: C.amber }}>I touch these every day.</span>
      </FadeUp>
      <FadeUp delay={210} style={{ fontSize: 40, color: C.dim, marginTop: 40 }}>
        Built by a machine operator, for every plant that can't afford a research lab.
      </FadeUp>
      <FadeUp delay={280} style={{ marginTop: 60, fontFamily: MONO, fontSize: 36 }}>
        <span style={{ color: C.amber }}>hellotravisss.github.io/mixmind/web</span>
        <span style={{ color: C.faint }}>   ·   github.com/Hellotravisss/mixmind</span>
      </FadeUp>
    </div>
  </Fill>
);

/* =============== timeline =============== */
export const Demo: React.FC = () => (
  <AbsoluteFill style={{ background: C.ground }}>
    <Series>
      <Series.Sequence durationInFrames={D.hook}><Hook /></Series.Sequence>
      <Series.Sequence durationInFrames={D.problem}><Problem /></Series.Sequence>
      <Series.Sequence durationInFrames={D.solution}><Solution /></Series.Sequence>
      <Series.Sequence durationInFrames={D.copilot}><Copilot /></Series.Sequence>
      <Series.Sequence durationInFrames={D.committee}><Committee /></Series.Sequence>
      <Series.Sequence durationInFrames={D.optimizer}><Optimizer /></Series.Sequence>
      <Series.Sequence durationInFrames={D.amd}><Amd /></Series.Sequence>
      <Series.Sequence durationInFrames={D.business}><Business /></Series.Sequence>
      <Series.Sequence durationInFrames={D.close}><Close /></Series.Sequence>
    </Series>
  </AbsoluteFill>
);
